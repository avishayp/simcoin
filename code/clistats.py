import logging
from bitcoin.rpc import JSONRPCError
import utils
import config


class CliStats:
    def __init__(self, context, writer):
        self._context = context
        self._writer = writer

    def execute(self):
        _persist_consensus_chain(self._calc_consensus_chain())
        self._persist_node_stats()

        logging.info('Executed cli stats')

    def _calc_consensus_chain(self):
        height = self._context.first_block_height
        nodes = self._context.nodes.values()
        consensus_chain = []
        logging.info(
            'Calculating consensus chain starting with height={}'.format(height))
        while True:
            block_hashes = {}
            failing_nodes = []
            block_hash = None
            for node in nodes:
                try:
                    block_hash = node.execute_rpc('getblockhash', height)
                    if block_hash in block_hashes:
                        block_hashes[block_hash].append(node.name)
                    else:
                        block_hashes[block_hash] = [node.name]
                except JSONRPCError:
                    failing_nodes.append(node.name)
            if len(failing_nodes) > 0:
                logging.info('Stopped calculating consensus chain on height={} because nodes={}'
                             ' have no block on this height'.format(height, failing_nodes))
                break
            elif len(block_hashes) > 1:
                logging.info('Stopped calculating consensus chain on height={} because'
                             ' nodes have different blocks ({})'.format(height, block_hashes))
                break
            else:
                consensus_chain.append(block_hash)
                height += 1

                logging.info(
                    'Added block with hash={} to consensus chain'.format(block_hash))

        logging.info('Calculated {} block long consensus chain from {} nodes and until height={}'
                     .format(len(consensus_chain), len(nodes), height - 1))
        return consensus_chain

    def _persist_node_stats(self):
        tips = []
        for node in self._context.nodes.values():
            tips.extend([Tip.from_dict(node.name, chain_tip)
                         for chain_tip in node.execute_rpc('getchaintips')])

        self._writer.write_csv(Tip.file_name, Tip.csv_header, tips)
        logging.info('Collected and persisted {} tips'.format(len(tips)))


def _persist_consensus_chain(chain):
    with open(config.consensus_chain_csv, 'w') as file:
        file.write('hash\n')
        file.writelines('\n'.join(chain))
        file.write('\n')


class Tip:
    __slots__ = ['_node', '_status', '_branchlen']

    csv_header = ['node', 'status', 'branchlen']
    file_name = 'tips.csv'

    def __init__(self, node, status, branchlen):
        self._node = node
        self._status = status
        self._branchlen = branchlen

    @classmethod
    def from_dict(cls, node, chain_tip):
        return cls(node, chain_tip['status'], chain_tip['branchlen'])

    def vars_to_array(self):
        return [self._node, self._status, self._branchlen]

import pytest
from clistats import CliStats
from mock import MagicMock
from bitcoin.rpc import JSONRPCError


@pytest.fixture
def setup(thing):
    thing.cli_stats = CliStats(thing.context, thing.writer)
    return thing


def test_calc_consensus_chain_first_node_no_block(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = JSONRPCError(
        {'code': -1, 'message': 'error'})
    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 0


def test_calc_consensus_chain_one_node(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = [
        'hash', JSONRPCError({'code': -1, 'message': 'error'})]

    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 1
    assert chain[0] == 'hash'


def test_calc_consensus_chain_multiple_nodes(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = [
        'hash1', 'hash2', JSONRPCError({'code': -1, 'message': 'error'})]
    node_1 = MagicMock()
    node_1.execute_rpc.side_effect = [
        'hash1', 'hash2', JSONRPCError({'code': -1, 'message': 'error'})]

    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0, '1': node_1}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 2
    assert chain[0] == 'hash1'
    assert chain[1] == 'hash2'


def test_calc_consensus_chain_one_node_trailing_back(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = ['hash1', 'hash2']
    node_1 = MagicMock()
    node_1.execute_rpc.side_effect = [
        'hash1', JSONRPCError({'code': -1, 'message': 'error'})]

    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0, '1': node_1}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 1
    assert chain[0] == 'hash1'


def test_calc_consensus_chain_different_chains(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = ['hash1', 'hash2', 'hash4']
    node_1 = MagicMock()
    node_1.execute_rpc.side_effect = ['hash1', 'hash3', 'hash4']

    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0, '1': node_1}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 1
    assert chain[0] == 'hash1'


def test_calc_consensus_chain_three_nodes(setup):
    node_0 = MagicMock()
    node_0.execute_rpc.side_effect = ['hash1', 'hash2', 'hash5']
    node_1 = MagicMock()
    node_1.execute_rpc.side_effect = ['hash1', 'hash3', 'hash4']
    node_2 = MagicMock()
    node_2.execute_rpc.side_effect = ['hash1', 'hash3', 'hash4']

    setup.context.first_block_height = 10
    setup.context.nodes = {'0': node_0, '1': node_1, '2': node_2}

    chain = setup.cli_stats._calc_consensus_chain()

    assert len(chain) == 1
    assert chain[0] == 'hash1'


def test_node_stats(setup):
    node_0 = MagicMock()
    node_0.name = 'name'
    node_0.execute_rpc.return_value = [
        {'status': 'active', 'branchlen': 2}]
    setup.context.nodes = {'0': node_0}

    setup.cli_stats._persist_node_stats()

    assert setup.writer.write_csv.call_args[0][1] == ['node', 'status', 'branchlen']
    assert len(setup.writer.write_csv.call_args[0][2]) == 1

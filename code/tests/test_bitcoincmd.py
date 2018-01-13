from cli import bitcoincmd
import config


def test_start():
    cmd = bitcoincmd.start('node-1', '1.1.1.1',
                           'image', '/path', ['ip1', 'ip2'])

    assert '  ' not in cmd


def test_rm_peers():
    cmd = bitcoincmd.rm_peers('node')

    assert '  ' not in cmd
    assert cmd == 'docker exec simcoin-node rm -f {}/regtest/peers.dat'.format(config.bitcoin_data_dir)

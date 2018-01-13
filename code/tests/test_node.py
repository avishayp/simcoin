import pytest
import node as node_utils
from mock import patch, MagicMock
from bitcoin.wallet import CBitcoinSecret
import bitcoin

bitcoin.SelectParams('regtest')


@pytest.fixture
def setup():
    return node_utils.BitcoinNode('node-1', 'group', 'ip', 'image', '/path')


@patch('node.BitcoinNode.execute_rpc')
def test_get_coinbase_variables(m_execute_rpc, setup):
    m_execute_rpc.side_effect = [
        [
            {"txid": 'tx_hash_1', 'address': 'address_hash_1', 'amount': 50},
            {"txid": 'tx_hash_2', 'address': 'address_hash_2', 'amount': 25}
        ],
        'cTCrrgVLfBqEZ1dxmCnEwmiEWzeZHU8uw3CNvLVvbT4CrBeDdTqc',
        'cTCrrgVLfBqEZ1dxmCnEwmiEWzeZHU8uw3CNvLVvbT4CrBeDdTqc'
    ]

    setup.create_tx_chains()

    assert m_execute_rpc.call_count == 3
    assert len(setup._tx_chains) == 2

    chain_1 = setup._tx_chains[0]
    assert chain_1.current_unspent_tx == 'tx_hash_1'
    assert chain_1.address == 'address_hash_1'
    assert chain_1.seckey == CBitcoinSecret('cTCrrgVLfBqEZ1dxmCnEwmiEWzeZHU8uw3CNvLVvbT4CrBeDdTqc')
    assert chain_1.amount == 5000000000

    chain_2 = setup._tx_chains[1]
    assert chain_2.current_unspent_tx == 'tx_hash_2'
    assert chain_2.address == 'address_hash_2'
    assert chain_2.amount == 2500000000


@patch('utils.sleep')
def test_wait_until_height_reached(m_sleep):
    node = MagicMock()
    node.execute_rpc.side_effect = ['0', '9', '10']
    node_utils.wait_until_height_reached(node, 10)

    assert m_sleep.call_count == 2


@patch('utils.sleep')
def test_wait_until_height_reached_already_reached(m_sleep):
    node = MagicMock()
    node.execute_rpc.return_value = '10'
    node_utils.wait_until_height_reached(node, 10)

    assert m_sleep.called is False

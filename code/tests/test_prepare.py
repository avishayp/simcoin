import pytest
from mock import patch, MagicMock, mock_open
import prepare
import config
import bitcoin

bitcoin.SelectParams('regtest')


@pytest.fixture
def setup(thing):
    thing.prepare = prepare.Prepare(thing.context)
    thing.prepare._pool = MagicMock()
    return thing


@patch('node.wait_until_height_reached', lambda node, height: None)
@patch('utils.sleep', lambda time: None)
@patch('prepare._calc_number_of_tx_chains', lambda txs_per_tick, block_per_tick, amount_of_nodes: 5)
def test_warmup_block_generation(setup):
    node_0 = MagicMock()
    node_1 = MagicMock()
    nodes = [node_0, node_1]
    setup.context.nodes.values.return_value = nodes
    setup.prepare._give_nodes_spendable_coins()

    assert node_0.execute_rpc.call_count == 2
    assert node_1.execute_rpc.call_count == 2


@patch('os.path.exists')
@patch('os.path.islink')
@patch('os.makedirs')
@patch('bash.check_output')
@patch('builtins.open', new_callable=mock_open)
def test_prepare_simulation_dir(m_open, m_check_output, m_makedirs, m_islink, m_exists, setup):
    m_exists.return_value = False
    setup.prepare._prepare_simulation_dir()

    assert m_makedirs.call_count == 3
    assert m_check_output.call_count == 10


@patch('bash.check_output')
def test_remove_old_containers_if_exists(m_check_output):
    m_check_output.return_value = ['container1', 'container2']
    prepare._remove_old_containers_if_exists()

    assert m_check_output.call_count == 2


@patch('bash.check_output')
def test_remove_old_containers_if_exists_no_old_containers(m_check_output):
    m_check_output.return_value = []
    prepare._remove_old_containers_if_exists()

    assert m_check_output.call_count == 1


@patch('utils.sleep', lambda t: None)
@patch('bash.call_silent')
@patch('bash.check_output')
def test_recreate_network(m_check_output, m_call_silent):
    m_call_silent.return_value = 0
    prepare._recreate_network()

    assert m_check_output.call_count == 2
    assert m_call_silent.call_count == 1


@patch('utils.sleep', lambda t: None)
@patch('bash.call_silent')
@patch('bash.check_output')
def test_recreate_network_no_network(m_check_output, m_call_silent):
    m_call_silent.return_value = -1
    prepare._recreate_network()

    assert m_check_output.call_count == 1


def test_calc_number_of_tx_chains():
    config.max_in_mempool_ancestors = 25
    amount = prepare._calc_number_of_tx_chains(2, 1 / 600, 10)

    assert amount == 51

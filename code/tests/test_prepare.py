from unittest import TestCase
from mock import MagicMock
from mock import patch
from mock import mock_open
import prepare
from prepare import Prepare
import config
import bitcoin
from mock import Mock


class TestPrepare(TestCase):

    def setUp(self):
        self.context = Mock()
        self.prepare = Prepare(self.context)

        bitcoin.SelectParams('regtest')

    @patch('node.wait_until_height_reached', lambda node, height: None)
    @patch('utils.sleep', lambda time: None)
    @patch('prepare._calc_number_of_tx_chains',
           lambda txs_per_tick, block_per_tick, amount_of_nodes: 5)
    def test_warmup_block_generation(self):
        node_0 = MagicMock()
        node_1 = MagicMock()
        nodes = [node_0, node_1]
        self.context.nodes.values.return_value = nodes

        self.prepare._pool = MagicMock()
        self.prepare._give_nodes_spendable_coins()

        self.assertEqual(node_0.execute_rpc.call_count, 2)
        self.assertEqual(node_1.execute_rpc.call_count, 2)

    @patch('os.path.exists')
    @patch('os.path.islink')
    @patch('os.makedirs')
    @patch('bash.check_output')
    @patch('builtins.open', new_callable=mock_open)
    def test_prepare_simulation_dir(
            self, m_open, m_check_output, m_makedirs, m_islink, m_exists):
        m_exists.return_value = False
        self.prepare._pool = MagicMock()

        self.prepare._prepare_simulation_dir()

        self.assertEqual(m_makedirs.call_count, 3)
        self.assertEqual(m_check_output.call_count, 10)

    @patch('bash.check_output')
    def test_remove_old_containers_if_exists(self, m_check_output):
        m_check_output.return_value = ['container1', 'container2']

        prepare._remove_old_containers_if_exists()

        self.assertEqual(m_check_output.call_count, 2)

    @patch('bash.check_output')
    def test_remove_old_containers_if_exists_no_old_containers(
            self, m_check_output):
        m_check_output.return_value = []

        prepare._remove_old_containers_if_exists()

        self.assertEqual(m_check_output.call_count, 1)

    @patch('utils.sleep', lambda t: None)
    @patch('bash.call_silent')
    @patch('bash.check_output')
    def test_recreate_network(self, m_check_output, m_call_silent):
        m_call_silent.return_value = 0

        prepare._recreate_network()

        self.assertEqual(m_check_output.call_count, 2)
        self.assertEqual(m_call_silent.call_count, 1)

    @patch('utils.sleep', lambda t: None)
    @patch('bash.call_silent')
    @patch('bash.check_output')
    def test_recreate_network_no_network(self, m_check_output, m_call_silent):
        m_call_silent.return_value = -1

        prepare._recreate_network()

        self.assertEqual(m_check_output.call_count, 1)

    def test_calc_number_of_tx_chains(self):
        config.max_in_mempool_ancestors = 25
        amount = prepare._calc_number_of_tx_chains(2, 1 / 600, 10)

        self.assertEqual(amount, 51)

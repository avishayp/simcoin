from unittest import TestCase
import bitcoindcmd


class TestBitcoindcmd(TestCase):

    def test_start_selfish_miner_private_node(self):
        cmd = bitcoindcmd.start_selfish_mining()

        self.assertTrue('  ' not in cmd)

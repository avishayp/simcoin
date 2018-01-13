import pytest
from simulationfiles import nodes_config as nc
from mock import patch


def test_check_if_share_sum_is_1_false():
    nodes = [
        nc.NodeConfig(
            'group',
            'node-0',
            0.4,
            0,
            None),
        nc.NodeConfig(
            'group',
            'node-1',
            0.4,
            0,
            None)]

    with pytest.raises(SystemExit) as cm:
        nc._check_if_share_sum_is_1(nodes)

    assert cm.value.code == -1


def test_check_if_share_sum_is_1_true():
    nodes = [
        nc.NodeConfig(
            'group',
            'node-0',
            0.4,
            0,
            None),
        nc.NodeConfig(
            'group',
            'node-1',
            0.6,
            0,
            None)]

    nc._check_if_share_sum_is_1(nodes)


@patch('bash.call_silent')
def test_check_if_image_exists_image_does_not_exists(m_call_silent):
    node_args = ['a', 'b', 'c', 'd', 'image']
    m_call_silent.return_value = -1

    with pytest.raises(SystemExit) as context:
        nc._check_if_image_exists(node_args)

    assert context.value.code == -1


@patch('bash.call_silent')
def test_wtf(m_call_silent):
    node_args = ['a', 'b', 'c', 'd', 'image']
    m_call_silent.return_value = 0

    nc._check_if_image_exists(node_args)

    assert m_call_silent.called is True
    assert m_call_silent.call_args[0][0] == 'docker inspect d', 'docker inspect image'

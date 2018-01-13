from simulationfiles import network_config
from mock import patch, mock_open
from textwrap import dedent
from simulationfiles.nodes_config import NodeConfig


def test_create_header():
    header = network_config._create_header([
        NodeConfig('group', 'node-1', 0, 0, None),
        NodeConfig('group', 'node-2', 0, 0, None)
    ])

    assert len(header) == 3
    assert header == ['', 'node-1', 'node-2']


def test_create_matrix_full_connection():
    header = ['', 'node-0', 'node-1', 'node-2']
    connectivity = 1

    matrix = network_config._create_matrix(header, connectivity)
    for i in range(1, len(header)):
        for j in range(1, i):
            if i != j:
                connection_between_nodes = matrix[i][j] + matrix[j][i]
                assert connection_between_nodes == 1


def test_create_matrix_no_connection():
    header = ['', 'node-0', 'node-1', 'node-2']
    connectivity = 0

    matrix = network_config._create_matrix(header, connectivity)
    for i in range(1, len(matrix)):
        for j in range(1, len(matrix)):
            if i != j:
                assert matrix[i][j] == 0


DATA_1 = dedent("""
    ,node-0,node-1,node-2
    node-0,1,1,0
    node-1,1,2,1
    node-2,0,1,3
    """).strip()


@patch("builtins.open", mock_open(read_data=DATA_1))
@patch('utils.check_for_file', lambda file: None)
def test_read_connections():
    connections = network_config.read_connections()

    assert len(connections.keys()) == 3

    assert connections['node-0'] == ['node-1']
    assert connections['node-1'] == ['node-0', 'node-2']
    assert connections['node-2'] == ['node-1']


def test_check_if_fully_connected_1():
    matrix = [
        ['', 'node-0', 'node-1'],
        ['node-0', 1, 0],
        ['node-1', 0, 1]
    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is False


def test_check_if_fully_connected_2():
    matrix = [
        ['', 'node-0', 'node-1'],
        ['node-0', 1, 1],
        ['node-1', 1, 1]
    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is True


def test_check_if_fully_connected_3():
    matrix = [
        ['', 'node-0', 'node-1', 'node-2'],
        ['node-0', 1, 0, 1],
        ['node-1', 0, 1, 1],
        ['node-2', 1, 1, 1]
    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is True


def test_check_if_fully_connected_4():
    matrix = [
        ['', 'node-0', 'node-1', 'node-2'],
        ['node-0', 1, 0, 1],
        ['node-1', 0, 1, 0],
        ['node-2', 1, 0, 1]
    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is False


def test_check_if_fully_connected_5():
    matrix = [
        ['', 'node-0', 'node-1', 'node-2', 'node-3'],
        ['node-0', 1, 0, 0, 1],
        ['node-1', 0, 1, 1, 0],
        ['node-2', 0, 1, 1, 0],
        ['node-3', 1, 0, 0, 1],

    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is False


def test_check_if_fully_connected_6():
    matrix = [
        ['', 'node-0', 'node-1', 'node-2', 'node-3'],
        ['node-0', 1, 1, 0, 0],
        ['node-1', 1, 1, 1, 0],
        ['node-2', 0, 1, 1, 0],
        ['node-3', 0, 0, 0, 1],

    ]
    fully_connected = network_config._check_if_fully_connected(matrix)
    assert fully_connected is False

import utils
from mock import patch, mock_open
from textwrap import dedent
from collections import namedtuple
from argparse import Namespace


@patch('builtins.exit')
@patch('os.path.isfile')
def test_check_for_files_file_not_existing(m_isfile, m_exit):
    m_isfile.return_value = False

    utils.check_for_file('file.txt')

    assert m_exit.called is True


@patch('builtins.exit')
@patch('os.path.isfile')
def test_check_for_files_file_exists(m_isfile, m_exit):
    m_isfile.return_value = True

    utils.check_for_file('file.txt')

    assert m_exit.called is False


@patch('os.path.isfile', lambda path: True)
def test_read():
    data = dedent("""
        int,float,string
        1,45.5,node-1
    """).strip()

    m = mock_open(read_data=data)
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
    with patch('builtins.open', m):
        data = utils.read_csv('/some.csv')[0]
        assert data.int == 1
        assert data.float == 45.5
        assert data.string == 'node-1'


def test_read_empty_file():
    m = mock_open(read_data='')
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
    with patch('builtins.open', m):
        data = utils.read_csv('/some.csv')
        assert data == []


@patch('utils.read_csv', lambda file: [])
@patch('builtins.open', new_callable=mock_open)
def test_update_args_1(m_open):
    utils.update_args(Namespace(int=1, float=1.1, string='test'))

    handle = m_open()
    assert handle.write.call_count == 2
    assert 'string' in handle.write.call_args_list[0][0][0]
    assert 'float' in handle.write.call_args_list[0][0][0]
    assert 'int' in handle.write.call_args_list[0][0][0]

    assert '1' in handle.write.call_args_list[1][0][0]
    assert '1.1' in handle.write.call_args_list[1][0][0]
    assert 'test' in handle.write.call_args_list[1][0][0]


@patch('utils.read_csv')
@patch('builtins.open', new_callable=mock_open)
def test_update_args_2(m_open, m_read):
    Args = namedtuple('Args', 'int float')
    m_read.return_value = [Args(2, 2.2)]

    utils.update_args(Namespace(int=1, string='test'))

    handle = m_open()
    assert handle.write.call_count == 2

    assert '1' in handle.write.call_args_list[1][0][0]
    assert '2.2' in handle.write.call_args_list[1][0][0]
    assert 'test' in handle.write.call_args_list[1][0][0]

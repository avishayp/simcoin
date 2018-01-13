import pytest
from event import Event, _calc_analyze_skip_ticks
from mock import patch, MagicMock, mock_open
from bitcoin.rpc import JSONRPCError
import logging

logging.disable(logging.CRITICAL)


@patch('time.time')
@patch('utils.sleep')
@patch('utils.check_for_file', lambda file: None)
def test_execute_multiple_cmds(m_sleep, m_time):
    m_file = mock_open(read_data=''.join(
        'cmd1,cmd2,cmd3'
    ))
    m_file.return_value.__iter__ = lambda self: self
    m_file.return_value.__next__ = lambda self: next(
        iter(self.readline, ''))

    with patch('builtins.open', m_file):
        mock = MagicMock()
        mock.args.tick_duration = 1
        e = Event(mock)
        e._execute_cmd = MagicMock()

        m_time.return_value = 0

        e.execute()

        assert e._execute_cmd.call_count == 3
        assert m_sleep.called is True


@patch('time.time')
@patch('utils.sleep')
@patch('utils.check_for_file', lambda file: None)
def test_execute_multiple_lines(m_sleep, m_time):
    m_file = mock_open(read_data=''.join(
        'cmd1\n'
        'cmd2'
    ))
    m_file.return_value.__iter__ = lambda self: self
    m_file.return_value.__next__ = lambda self: next(
        iter(self.readline, ''))

    with patch('builtins.open', m_file):
        mock = MagicMock()
        mock.args.tick_duration = 1
        e = Event(mock)
        e._execute_cmd = MagicMock()

        m_time.return_value = 0

        e.execute()

        assert e._execute_cmd.call_count == 2
        assert m_sleep.call_count == 2


@patch('utils.check_for_file', lambda file: None)
@patch('logging.error')
def test_execute_with_exce_execute_cmd(m_error):
    m_file = mock_open(read_data=''.join(
        'cmd1'
    ))
    m_file.return_value.__iter__ = lambda self: self
    m_file.return_value.__next__ = lambda self: next(
        iter(self.readline, ''))

    with patch('builtins.open', m_file):
        mock = MagicMock()
        mock.args.tick_duration = 0
        e = Event(mock)
        e._execute_cmd = MagicMock()
        e._execute_cmd.side_effect = Exception('mock')

        e.execute()
        assert m_error.call_args[0][0].startswith('Simulation could not') is True


def test_execute_cmd_with_block_cmd():
    node_1 = MagicMock()
    cmd = 'block node-1'
    e = Event(MagicMock())
    e._context.nodes = {'node-1': node_1}
    e._execute_cmd(cmd)

    assert node_1.generate_blocks.called is True


def test_execute_cmd_with_block_cmd_with_empty_cmd():
    node_1 = MagicMock()

    e = Event(MagicMock())
    e.generate_tx = MagicMock()
    e._execute_cmd('')

    assert node_1.execute_rpc.called is False
    assert e.generate_tx.called is False


def test_execute_cmd_with_tx_tmd():
    node = MagicMock()
    cmd = 'tx node-1'

    e = Event(MagicMock())
    e.generate_tx = MagicMock()
    e._context.nodes = {'node-1': node}
    e._execute_cmd(cmd)

    assert node.generate_tx.called is True


def test_execute_cmd_with_unknown_cmd():
    cmd = 'unknown node-1'
    e = Event(MagicMock())
    e._context.nodes = {'node-1': {}}

    with pytest.raises(Exception) as context:
        e._execute_cmd(cmd)

    assert 'Unknown cmd' in str(context)


def test_execute_cmd_with_exception():
    context = MagicMock()
    node = MagicMock()
    node.generate_tx.side_effect = JSONRPCError(
        {'code': -1, 'message': 'test_message'})
    context.nodes = {'node-1': node}

    e = Event(context)
    e._execute_cmd('tx node-1')


def test_calc_analyze_skip_ticks_1():
    tick_count = _calc_analyze_skip_ticks(.1, 50)
    assert tick_count == 10


def test_calc_analyze_skip_ticks_2():
    tick_count = _calc_analyze_skip_ticks(.1, .05)
    assert tick_count == 20


def test_calc_analyze_skip_ticks_3():
    tick_count = _calc_analyze_skip_ticks(100, 50)
    assert tick_count == 1

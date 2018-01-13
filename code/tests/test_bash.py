import bash
from mock import patch
from mock import mock_open


@patch('subprocess.check_output')
def test_check_output(mock):
    mock.return_value = b'test\ntest\ttest\t\n\n'

    output = bash.check_output('cmd')

    assert output == 'test\ntest\ttest'


@patch("builtins.open", mock_open())
@patch('subprocess.call')
def test_call_silent(mock):
    mock.return_value = b'test'
    output = bash.call_silent('cmd')

    assert str(output, 'utf-8') == 'test'

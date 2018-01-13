import pytest
from mock import Mock, mock_open, patch
from write import Writer
import config


@pytest.fixture
def setup(thing):
    thing.writer = Writer('test_tag')
    return thing


@patch('fcntl.flock', lambda file, lock: None)
@patch('builtins.open', new_callable=mock_open)
def test_write_csv(m_open, setup):
    elements = Mock()
    elements.vars_to_array.return_value = ['content_1', 'content_2']
    setup.writer.write_csv(
        'file.name', [
            'header_1', 'header_2'], [elements])

    assert m_open.call_count == 2
    assert m_open.call_args_list[0][0] == (config.postprocessing_dir + 'file.name', 'w')
    assert m_open.call_args_list[1][0] == (config.postprocessing_dir + 'file.name', 'a')

    handle = m_open()
    assert handle.write.call_args_list[0][0][0] == 'header_1,header_2,tag\r\n'
    assert handle.write.call_args_list[1][0][0] == 'content_1,content_2,test_tag\r\n'

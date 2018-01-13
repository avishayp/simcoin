import pytest
from mock import patch, mock_open
from postprocessing import PostProcessing
import postprocessing
from textwrap import dedent


@pytest.fixture
def setup(thing):
    thing.postprocessing = PostProcessing(thing.context, thing.writer)
    return thing


def test_cut_log(setup):
    data = dedent("""
        line1
        line2 start
        line3
        line4 end
        line5
    """).strip()

    m = mock_open(read_data=''.join(data))
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
    with patch('builtins.open', m) as m_open:
        postprocessing._extract_from_file(
            'source_file', 'destination_file', 'start', 'end')

        assert m_open.call_count == 2
        assert m_open.call_args_list[0][0][0] == 'source_file'
        assert m_open.call_args_list[1][0][0] == 'destination_file'

        handle = m_open()
        assert handle.write.call_args_list[0][0][0] == 'line2 start\n'
        assert handle.write.call_args_list[1][0][0] == 'line3\n'
        assert handle.write.call_args_list[2][0][0] == 'line4 end\n'

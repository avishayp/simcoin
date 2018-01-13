import sys
import os

import pytest
from mock import MagicMock

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


class Obj:
    pass


@pytest.fixture
def thing():
    obj = Obj()
    obj.context = MagicMock()
    obj.writer = MagicMock()
    return obj

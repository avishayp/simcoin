import pytest
from simulationfiles import checkargs
import argparse


def test_check_positive():
    value = checkargs.check_positive(0)
    assert value == 0


def test_check_positive_exception():
    with pytest.raises(argparse.ArgumentTypeError) as context:
        checkargs.check_positive(-1)

    assert '-1 is an invalid positive value' in str(context)


def test_check_percentage_zero():
    value = checkargs.check_percentage(0)
    assert value == 0


def test_check_percentage_one():
    value = checkargs.check_percentage(1)
    assert value, 1


def test_check_percentage_negative():
    with pytest.raises(argparse.ArgumentTypeError) as context:
        checkargs.check_percentage(-0.1)
    assert '-0.1 is an invalid percentage value [0,1]' in str(context)


def test_check_percentage_over_one():
    with pytest.raises(argparse.ArgumentTypeError) as context:
        checkargs.check_percentage(1.1)
    assert '1.1 is an invalid percentage value [0,1]' in str(context)


def test_check_percentage_with_string():
    with pytest.raises(ValueError):
        checkargs.check_percentage('test')


def test_check_positive_float():
    value = checkargs.check_positive(1.1)
    assert value == 1.1


def test_check_positive_float_with_string():
    with pytest.raises(ValueError):
        checkargs.check_positive_float('test')


def test_check_positive_int_with_float():
    with pytest.raises(argparse.ArgumentTypeError) as context:
        checkargs.check_positive_int(1.1)
    assert '1.1 is an invalid integer' in str(context)


def test_check_positive_int():
    checkargs.check_positive_int('10')

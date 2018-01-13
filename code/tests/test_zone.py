import pytest
import ipaddress
from simulationfiles.zone import Zone


@pytest.fixture
def setup(thing):
    thing.zone = Zone()
    return thing


def test_get_ip(setup):
    ip = setup.zone.get_ip(100)

    assert ip == ipaddress.IPv4Address('240.1.0.1')
    assert setup.zone.zones[100].latency == 100
    assert setup.zone.zones[100].network == ipaddress.ip_network('240.1.0.0/16')


def test_get_ip_second_time_same_latency(setup):
    setup.zone.get_ip(100)
    ip = setup.zone.get_ip(100)

    assert ip == ipaddress.IPv4Address('240.1.0.2')


def test_get_ip_second_time_different_latency(setup):
    setup.zone.get_ip(100)
    ip = setup.zone.get_ip(0)

    assert ip == ipaddress.IPv4Address('240.2.0.1')

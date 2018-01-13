import ipaddress
from cli import tccmd
from simulationfiles.zone import ZoneConfig


def test_create():
    zones = {
        0: ZoneConfig(ipaddress.ip_network('240.1.0.0/16'), ipaddress.ip_network('240.1.0.0/16').hosts(), 0),
        100: ZoneConfig(ipaddress.ip_network('240.2.0.0/16'), ipaddress.ip_network('240.2.0.0/16').hosts(), 100),
        200: ZoneConfig(ipaddress.ip_network('240.3.0.0/16'), ipaddress.ip_network('240.3.0.0/16').hosts(), 200),
    }

    cmds = tccmd.create('node-0', zones, 100)[0]

    assert 'add dev eth0' in cmds
    assert 'u32 match ip dst 240.1.0.0/16 flowid 1:2' in cmds
    assert 'u32 match ip dst 240.2.0.0/16 flowid 1:3' in cmds
    assert 'u32 match ip dst 240.3.0.0/16 flowid 1:4' in cmds
    assert '1:1 handle 10: netem delay 0ms' in cmds
    assert '1:2 handle 20: netem delay 100ms' in cmds
    assert '1:3 handle 30: netem delay 100ms' in cmds
    assert '1:4 handle 40: netem delay 300ms' in cmds

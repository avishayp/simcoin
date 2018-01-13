from systemmonitor import CpuTimeSnapshot
from systemmonitor import MemorySnapshot


def test_cpu_time_snapshot_from_bash():
    cpu_time = 'cpu  6993159 247853 1473357 6905504 50921 0 102406 0 0 0'

    snapshot = CpuTimeSnapshot.from_bash(cpu_time)

    assert snapshot._user == '6993159'
    assert snapshot._nice == '247853'
    assert snapshot._system == '1473357'
    assert snapshot._idle == '6905504'


def test_memory_snapshot_from_bash():
    memory = 'MemTotal:        7577060 kB\nMemFree:         8316 kB\nMemAvailable:         1568016 kB'

    snapshot = MemorySnapshot.from_bash(memory)

    assert snapshot._total == '7577060'
    assert snapshot._available == '1568016'

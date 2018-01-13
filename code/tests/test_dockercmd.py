from cli import dockercmd


def test_run_node():
    cmd = dockercmd.run_node('node-1', '1.1.1.1', 'image', 'cmd', '/path')

    assert '  ' not in cmd

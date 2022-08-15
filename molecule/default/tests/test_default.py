import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_directories(host):
    dirs = [
        "/etc/loki"
    ]
    for dir in dirs:
        d = host.file(dir)
        assert d.is_directory
        assert d.exists


def test_files(host):
    files = [
        "/etc/systemd/system/loki.service",
        "/usr/local/bin/loki",
        "/etc/loki/loki-config.yml",
    ]
    for file in files:
        f = host.file(file)
        assert f.exists
        assert f.is_file


def test_service(host):
    s = host.service("loki")
    assert s.is_enabled
    assert s.is_running


def test_socket(host):
    sockets = [
        "tcp://0.0.0.0:3100"
    ]
    for socket in sockets:
        s = host.socket(socket)
        assert s.is_listening
import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

@pytest.mark.parametrize("name", [
    "rh-mariadb103",
    "MySQL-python",
    "perl-DBD-MySQL",
])
def test_mysql_packages_installed(host, name):
    pkg = host.package(name)
    assert pkg.is_installed

def test_mysql_listening(host):
    socket = host.socket("tcp://127.0.0.1:3306")
    assert socket.is_listening

def test_mysql_user(host):
    cmd = 'mysql -u root -proot -e "select user from mysql.user;"'
    out = host.check_output(cmd)
    assert "jdoe" in out

def test_mysql_database(host):
    cmd = 'mysql -u root -proot -e "show databases;"'
    out = host.check_output(cmd)
    assert "example" in out

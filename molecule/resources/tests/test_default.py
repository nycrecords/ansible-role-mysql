import os
import pytest
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")

@pytest.mark.parametrize("name", [
    "rh-php72",
    "rh-php72-php-devel",
    "rh-php72-php-fpm",
    "rh-php72-php-gd",
    "rh-php72-php-ldap",
    "rh-php72-php-mbstring",
    "rh-php72-php-opcache",
    "rh-php72-php-pdo",
    "rh-php72-php-pecl-apcu",
    "rh-php72-php-xmlrpc",
])
def test_php_packages_installed(host, name):
    pkg = host.package(name)
    assert pkg.is_installed

def test_fpm_service(host):
    service = host.service("rh-php72-php-fpm")
    assert service.is_running
    assert service.is_enabled

def test_php_info_version(host):
    cmd = 'curl localhost/test.php'
    out = host.check_output(cmd)
    assert re.search('PHP Version 7.2.24', out)

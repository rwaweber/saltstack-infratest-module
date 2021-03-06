# saltstack-infratest-module
[![Build Status](https://travis-ci.org/ssplatt/saltstack-infratest-module.svg?branch=master)](https://travis-ci.org/ssplatt/saltstack-infratest-module)
[![Code Climate](https://codeclimate.com/github/ssplatt/saltstack-infratest-module/badges/gpa.svg)](https://codeclimate.com/github/ssplatt/saltstack-infratest-module)
[![Test Coverage](https://codeclimate.com/github/ssplatt/saltstack-infratest-module/badges/coverage.svg)](https://codeclimate.com/github/ssplatt/saltstack-infratest-module/coverage)

A Salt module using the testinfra python module for compliance testing and auditing. This allows you to take advantage of the many features of Salt, like the yaml merging for configuration and the database of servers to test.

## Testinfra
Testinfra is a python module created to test your infrastructure. For more info:
 - http://testinfra.readthedocs.org/en/latest/
 - https://github.com/philpep/testinfra

This module must be installed on each system you wish to test.  To install:
```
# pip install testinfra
```

## Install
There is a simple Salt formula available at https://github.com/ssplatt/infratest-formula.

To manually install the module, place `infratest.py` in the salt modules directory. By default this is `/srv/salt/_modules`. Then, run `salt \* saltutil.sync_modules` to copy the module to all nodes.

## Configure
This module loads configuration data from pillar so you can maintain it as you would any other server definition. For simple usage, create a `pillar/infratest` directory and place the `default.sls` inside it.  Then, in your `pillar/top.sls` file, configure a section to use `infratest.default`.  You can create other sls configuration files so you can overwrite and merge configurations for other servers. For example:

```yaml
# pillar/top.sls

base:
  '*':
    - infratest.default

  'web*':
    - infratest.web
```

```yaml
# pillar/infratest/default.sls

infratest:
  file:
    '/etc/passwd':
      exists: true
```

```yaml
# pillar/infratest/web.sls

infratest:
  file:
    '/etc/httpd':
      exists: true
```

The yaml should merge so that all servers will check for `/etc/passwd` to exist and servers beginning with `web` will also check for `/etc/httpd` to exist. To confirm that your pillar data is merging the way you expect it, run `salt \* pillar.get infratest` on your salt-master. `salt \* saltutil.refresh_pillar` may be needed to refresh the pillar on all devices after changes have been made.

## Usage
### All Tests
Default is abbreviated output

`# salt \* infratest.run_all`
```
salt-master.mycorp.com:
    ----------
    Fail:
        1
    Pass:
        6
```

### All Tests with verbose output
`# salt \* infratest.run_all details=True`
```
salt-master.mycorp.com:
    ----------
    Failed:
        - sshd is enabled: True
    Passed:
        - /etc/passwd exists: True
        - /etc/passwd is: file
        - /etc/passwd is owned by user: root
        - /etc/passwd is owned by group: root
        - /etc/passwd has mode: 0644
        - /etc/passwd contains: root
    Totals:
        ----------
        Fail:
            1
        Pass:
            6
```

### A Single Test
`# salt \* infratest.file_mode /etc/passwd 0644`

```
salt-master.mycorp.com:
    ----------
    Failed:
    Passed:
        - /etc/passwd has mode: 0644
```

## TODO
 1. [Process tests](http://testinfra.readthedocs.org/en/latest/modules.html#process)
 2. [LocalCommand tests](http://testinfra.readthedocs.org/en/latest/modules.html#localcommand)
 3. [Socket clients tests](http://testinfra.readthedocs.org/en/latest/modules.html#testinfra.modules.Socket.clients)
 4. [Socket get_listening_sockets tests](http://testinfra.readthedocs.org/en/latest/modules.html#testinfra.modules.Socket.get_listening_sockets)


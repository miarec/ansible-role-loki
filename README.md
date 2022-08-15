# ansible role to install Grafana Loki
This ansible role will install the Grafana Loki Logging Engine locally detailed [here](https://grafana.com/docs/loki/latest/installation/local/)

## Overview
 - Loki Release will be:
    - Downloaded from github repository
    - Inflated
    - Renamed and moved to `/usr/local/bin`
    - Made executable
 - Config File will be created
 - Version File will be creaed
 - SystemD service will be
    - created
    - started
    - enabled

## Example Playbook

```yaml
- hosts: loki

  vars:
    loki_local_storage_dir: "etc/loki"
    loki_version: "2.4.2"

  roles:
    - loki
```

## Whats with the Verison file?
Eagle eyed engineers might have noticed that the version file action is not part of the Grafana Loki documentation

In order to allow for idempotency, not only do we need to check that Loki is install and running, we need to verify the version,  this is a challenge because loki is not installed with a traditional package manager like `apt` or `yum`.

To resolve this, part of the install process is to create a file that contains the installed version,   this file can be read and registered to a variable `__loki_version` that can be verified against input variable `loki_version`

## CICD
A Github Action is configured to test this module everytime there is a push to the master branch or on pull requests

The following items are tested
- `yamllint` to verify proper yaml syntax
- `ansible-lint` to verify proper ansible syntax
- `molecule` testing
- Deploy playbook against docker containers with following distros
```
matrix:
  distro:
    - centos7
    - centos8
    - ubuntu1804
    - ubuntu2004
```
- Run `testinfra` testing against each container for the following
  - all directories are present
  - all files are present
  - loki service is running and enabled
  - server is listening on the configured port


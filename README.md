![GitHub Release](https://img.shields.io/github/v/release/uliegecsm/system-helpers)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/uliegecsm/system-helpers/test.yml)
![GitHub License](https://img.shields.io/github/license/uliegecsm/system-helpers)

[![PyPI - Version](https://img.shields.io/pypi/v/system-helpers?color=blue)](https://pypi.org/project/system-helpers/)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/system-helpers)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/system-helpers)

# System helpers

This repository contains useful standalone helper scripts for `Linux` systems.

## `apt`

Useful for dealing with `apt` related tasks.

For instance, the following command
```bash
apt-helpers install-packages --update --upgrade --clean --packages git wget
```
will perform:
1. `apt update`
2. `apt upgrade`
3. `apt --yes --no-install-recommends install git wget`
4. `apt clean && rm -rf /var/lib/apt/lists`

## `update-alternatives`

Useful for dealing with `update-alternatives` tasks.

# SOPROS OSA Backend

[![PyPI - Version](https://img.shields.io/pypi/v/sopros-osa-backend.svg)](https://pypi.org/project/sopros-osa-backend)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sopros-osa-backend.svg)](https://pypi.org/project/sopros-osa-backend)

---

**Table of Contents**

- [Description](#description)
- [Installation](#installation)
- [License](#license)

## Description

The project is the backend for calculating the social protection of elite athletes.
It based on the [SOPROS project](https://www.dshs-koeln.de/en/institute-of-european-sport-development-and-leisure-studies/research-projects/ongoing-projects/sopros/).
It provides an API to calculate the claims.

## Installation

### Development

For development you need to install [hatch](https://hatch.pypa.io/latest/install/)

```console
# start dev Server
hatch run serve

# run all tests
hatch run test
```

### Imagebuild

For the imagebuild you need to install [podman](https://podman.io/docs/installation)

Build image with podman

```console
# build image with podman
hatch run imagebuild

# start image
hatch run imagestart
```

Wichtige Links:
| Name | URL |
|---------|----------------------------|
| API Doc | http://127.0.0.1:8000/docs |

## License

`sopros-osa-backend` is distributed under the terms of the [TODO](LICENSE.md) license.

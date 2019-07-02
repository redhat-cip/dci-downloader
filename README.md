# DCI Downloader

`dci-downloader` is a useful tool for downloading the latest versions of Red Hat products

## TLDR

```console
$ yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ yum -y install dci-downloader
$ mv /etc/dci-downloader/dcirc.sh.dist /etc/dci-downloader/dcirc.sh
$ vi /etc/dci-downloader/dcirc.sh
$ LOCAL_STORAGE_FOLDER="/var/www/html" sudo dci-downloader --topic "RHEL-7.7"
```

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## Requirements

### Red Hat SSO

DCI is connected to the Red Hat SSO. You will need a [Red Hat account](https://access.redhat.com/).

### Remoteci

A remoteci is a Virtual Machine or a baremetal server running RHEL.
You should check that your remoteci:

- Is running the latest RHEL 7 release.
- Has a static IPv4 address.
- Has 160GB of free space in `/var`.
- Should be able to reach:
  - `https://api.distributed-ci.io` (443).
  - `https://packages.distributed-ci.io` (443).
  - `https://registry.distributed-ci.io` (443).
  - `https://quay.io` (443).
  - RedHat CDN.

## Installation

The `dci-downloader` is packaged and available as a RPM files.

```console
$ yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ yum -y install dci-downloader
```

## Configuration

### Remoteci creation

DCI is connected to the Red Hat SSO. You need to log in `https://www.distributed-ci.io` with your redhat.com SSO account.
Your user account will be created in our database the first time you connect.

After the first connection you can create a remoteci. Go to [https://www.distributed-ci.io/remotecis](https://www.distributed-ci.io/remotecis) and click `Create a new remoteci` button. Once your `remoteci` is created, you can retrieve the connection information in the `Authentication` column. Edit the `/etc/dci-downloader/dcirc.sh.dist` file with the information displayed and rename it to `/etc/dci-downloader/dcirc.sh`.

At this point, you can validate your credentials with the following commands:

```console
$ source /etc/dci-downloader/dcirc.sh
$ dcictl remoteci-list
```

If you see your remoteci in the list, everything is working great so far.

### Topic access

Before using dci-downloader, we need to check the list of topic (version of the product) you have access to:

```console
$ source /etc/dci-downloader/dcirc.sh
$ dcictl topic-list
```

If you don't see any topic then **you should contact your EPM at Red Hat** which will give you access to the topic you need.

## Usage

You can now download the latest version of a product using dci-downloader

```console
$ su - dci -s /bin/bash
$ sudo dci-downloader --topic "RHEL-7.7"
```

Product will be downloaded in `/var/lib/dci`. You can customize this changing the `LOCAL_STORAGE_FOLDER` env variable

```console
$ LOCAL_STORAGE_FOLDER="/var/www/html" sudo dci-downloader --topic "RHEL-7.7"
```

## License

Apache License, Version 2.0 (see [LICENSE](LICENSE) file)

## Contact

Email: Distributed-CI Team <distributed-ci@redhat.com>
IRC: #distributed-ci on Freenode

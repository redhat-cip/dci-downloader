# DCI Downloader

`dci-downloader` is a useful tool for downloading the latest versions of Red Hat products

## TLDR

```console
$ sudo yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ sudo yum -y install dci-downloader
$ source ~/dcirc.sh
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64"
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
$ sudo yum -y install https://packages.distributed-ci.io/dci-release.el7.noarch.rpm
$ sudo yum -y install dci-downloader python-dciclient
```

## Configuration

### Remoteci creation

DCI is connected to the Red Hat SSO. You need to log in `https://www.distributed-ci.io` with your redhat.com SSO account. Your user account will be created in our database the first time you connect.

After the first connection you can create a remoteci. Go to [https://www.distributed-ci.io/remotecis](https://www.distributed-ci.io/remotecis) and click `Create a new remoteci` button. Once your `remoteci` is created, you can retrieve the connection information in the `Authentication` column. Save those information in `~/dcirc.sh` file.

At this point, you can validate your credentials with the following commands:

```console
$ source ~/dcirc.sh
$ dcictl remoteci-list
```

If you see your remoteci in the list, everything is working great so far.

### Topic access

Before using dci-downloader, we need to check the list of topic (version of the product) you have access to:

```console
$ source ~/dcirc.sh
$ dcictl topic-list
```

If you don't see any topic then **you should contact your EPM at Red Hat** which will give you access to the topic you need.

## Usage

You can now download the latest version of a product using dci-downloader

```console
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64"
```

Product will be downloaded in `/var/lib/dci`. You can customize this changing the `DCI_LOCAL_REPO` env variable

```console
$ export DCI_LOCAL_REPO="/var/www/html"
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64"
```

## Options

By default dci-downloader will download all variants for x86_64 architecture without debug RPMs.


### Download other architectures

To download a specific architecture you can specify those using `--arch` option

```console
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64" --arch "ppc64le"
```

### Specific variants

To download only specific variants you can specify those using `--variant`

```console
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64" --variant "AppStream" --variant "BaseOS"
```

### Debug RPMs

To download debug RPMs you can add the `--debug` flag

```console
$ dci-downloader --topic "RHEL-8.0" --arch "x86_64" --debug
```

### Settings file

You can use a settings file to send parameters to configure dci-downloader.

Use `--settings` parameter:

```console
$ dci-downloader --settings "/etc/dci-rhel-agent/settings.yml"
```

All settings from settings.yml file will overwrite cli parameters.

Examples of a settings file:

```yaml
topic: RHEL-7
variants:
  - AppStream
  - BaseOS
archs:
  - x86_64
  - ppc64le
with_debug: false
```


## License

Apache License, Version 2.0 (see [LICENSE](LICENSE) file)


## Help

If something is not working correctly, ensure you have the latest version installed

```console
$ dci-downloader --version
$ dci-downloader --help
```

## Contact

Email: Distributed-CI Team <distributed-ci@redhat.com>
IRC: #distributed-ci on Freenode

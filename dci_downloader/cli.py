#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from dci_downloader import version

EXAMPLES = """
examples:
  # download topic RHEL-8.1
  dci-downloader --topic "RHEL-8.1"
  # download specific arch
  dci-downloader --topic "RHEL-8.1" --arch ppc64le
  # download explicit variants
  dci-downloader --topic "RHEL-8.1" --variant BaseOs  --variant AppStream
  # download eveything
  dci-downloader --all
"""

COPYRIGHT = """
copyright:
  Copyright © 2019 Red Hat.
  Licensed under the Apache License, Version 2.0
"""


def parse_arguments(arguments):
    parser = argparse.ArgumentParser(
        usage="dci-downloader --topic [TOPIC_NAME] [OPTIONS]",
        description="Downloader for Red Hat product",
        epilog=EXAMPLES + COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-v", "--version", action="version", version=version)
    parser.add_argument(
        "--debug", help="Add debug RPMs", dest="with_debug", action="store_true"
    )
    parser.add_argument(
        "--all",
        "--download-everything",
        help="Download everything",
        dest="download_everything",
        action="store_true",
    )
    parser.add_argument(
        "-t",
        "--topic",
        action="append",
        dest="topics_names",
        default=[],
        help="Topic name",
    )
    parser.add_argument(
        "--variant", action="append", dest="variants", default=[], help="Variant name"
    )
    parser.add_argument(
        "--arch", action="append", dest="archs", default=[], help="Architecture name"
    )
    parsed_arguments = parser.parse_args(arguments)
    if not parsed_arguments.archs:
        parsed_arguments.archs = ["x86_64"]
    parsed_arguments.archs = list(set(parsed_arguments.archs))
    return vars(parsed_arguments)

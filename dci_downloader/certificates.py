import os
import sys

from dci_downloader import api
from dci_downloader.fs import create_parent_dir


def _generate_key_and_cert(topic_info):
    keys = api.get_keys(topic_info["remoteci_id"])
    if keys is None:
        print("Can't get certificate's keys, contact DCI administrator")
        sys.exit(1)

    dci_cert_file = topic_info["dci_cert_file"]
    create_parent_dir(dci_cert_file)

    key = keys["key"]
    dci_key_file = topic_info["dci_key_file"]
    with open(dci_key_file, "w") as f:
        f.write(key)

    cert = keys["cert"]
    with open(dci_cert_file, "w") as f:
        f.write(cert)


def configure_ssl_certificates(topic_info):
    dci_key_file = topic_info["dci_key_file"]
    dci_cert_file = topic_info["dci_cert_file"]
    if os.path.exists(dci_key_file) and os.path.exists(dci_cert_file):
        if not api.cert_is_valid(dci_cert_file):
            _generate_key_and_cert(topic_info)
    else:
        _generate_key_and_cert(topic_info)

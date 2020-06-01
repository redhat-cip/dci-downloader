import os
import sys
import api

from dci_downloader.fs import create_parent_dir


def configure_ssl_certificates(settings):
    dci_key_file = settings.get("dci_key_file")
    dci_cert_file = settings.get("dci_cert_file")
    if not os.path.exists(dci_key_file) or not os.path.exists(dci_cert_file):
        keys = api.get_keys(settings["remoteci_id"])
        if keys is None:
            print("Can't get certificate's keys, contact DCI administrator")
            sys.exit(1)

        create_parent_dir(dci_cert_file)

        key = keys["key"]
        with open(dci_key_file, "w") as f:
            f.write(key)

        cert = keys["cert"]
        with open(dci_cert_file, "w") as f:
            f.write(cert)

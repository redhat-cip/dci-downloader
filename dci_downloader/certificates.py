import os
import sys
import api

from dci_downloader.fs import create_parent_dir


def configure_ssl_certificates(settings):
    dci_cert_file = settings.get("dci_cert_file")
    if not os.path.exists(dci_cert_file):
        keys = api.get_keys(settings["remoteci_id"])
        if keys is None:
            print("Can't get certificate's keys, contact DCI administrator")
            sys.exit(1)

        cert = keys["cert"]
        key = keys["key"]
        create_parent_dir(dci_cert_file)
        with open(dci_cert_file, "w") as f:
            f.write(key)
            f.write("\n")
            f.write(cert)

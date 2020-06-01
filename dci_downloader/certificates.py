import os
import sys
import api


def configure_ssl_certificates(settings, env_variables):
    download_ssl_certificates(settings)
    env_variables["REQUESTS_CA_BUNDLE"] = settings.get("dci_cert_file")


def download_ssl_certificates(settings):
    dci_cert_file = settings.get("dci_cert_file")
    if not os.path.exists(dci_cert_file):
        keys = api.get_keys(settings["remoteci_id"])
        if keys is None:
            print("Can't get certificate's keys, contact DCI administrator")
            sys.exit(1)

        cert = keys["cert"]
        key = keys["key"]
        with open(dci_cert_file, "w") as f:
            f.write(key)
            f.write("\n")
            f.write(cert)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from tempfile import NamedTemporaryFile

import requests
from dciclient.v1.api.context import build_signature_context

from api import extend_dci_topic_with_control_server_info, get_components, get_keys
from cli import parse_arguments
from stats import enough_space

from downloader import download


def verify_env_variables_needed_are_setted():
    expected_env_variables = ["DCI_CLIENT_ID", "DCI_API_SECRET", "DCI_CS_URL"]
    for env_variable in expected_env_variables:
        if env_variable not in os.environ:
            print("Ensure %s variables are set" % ",".join(expected_env_variables))
            sys.exit(1)


def create_temp_file(content):
    cert = NamedTemporaryFile(delete=False)
    cert.write(content)
    cert.close()
    return cert


def main():
    verify_env_variables_needed_are_setted()
    remoteci_id = os.getenv("DCI_CLIENT_ID").split("/")[1]
    context = build_signature_context()
    keys = get_keys(context, remoteci_id)
    if keys is None:
        print("Can't get certificate's keys, contact dci administrator")
        sys.exit(0)

    arguments = parse_arguments(sys.argv[1:])
    topics = arguments["topics"].values()
    has_error = False
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    for topic in topics:
        topic = extend_dci_topic_with_control_server_info(context, topic)
        if topic is None:
            has_error = True
            continue
        url = "https://repo.distributed-ci.io/%s/%s" % (
            topic["product_id"],
            topic["id"],
        )
        for component in get_components(context, topic):
            print("Download %s" % component["name"])
            base_url = "%s/%s" % (url, component["id"])
            files_list_url = "%s/dci_files_list.json" % base_url
            r = requests.get(files_list_url, cert=(cert, key))
            if r.status_code != 200:
                print(
                    "Can't get dci_files_list.json file! HTTP error code=%s, message=%s"
                    % (r.status_code, r.text)
                )
                continue
            files_list = r.json()
            container_storage_folder = "/var/lib/dci"
            host_storage_folder = os.getenv(
                "LOCAL_STORAGE_FOLDER", container_storage_folder
            )
            if not enough_space(files_list, container_storage_folder):
                print(
                    "Not enough space in %s skipping %s"
                    % (host_storage_folder, component["name"])
                )
                continue
            local_repo_path = "%s/%s/%s" % (
                container_storage_folder,
                topic["name"],
                component["name"],
            )
            download(base_url, files_list, local_repo_path, cert, key)
    os.unlink(cert)
    os.unlink(key)
    return_code = 1 if has_error else 0
    sys.exit(return_code)


if __name__ == "__main__":
    main()

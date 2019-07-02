#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from tempfile import NamedTemporaryFile

import requests
from dciclient.v1.api.context import build_signature_context

from api import get_topic, get_components, get_keys
from cli import parse_arguments
from stats import enough_space
from filters import filter_files_list
from downloader import download
from fs import mkdir_p


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
    has_error = False
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    for topic_name in arguments["topics_names"]:
        topic = get_topic(context, topic_name)
        if topic is None:
            has_error = True
            continue
        url = "https://repo.distributed-ci.io/%s/%s" % (
            topic["product_id"],
            topic["id"],
        )
        for component in get_components(context, topic):
            component_name = component["name"]
            print("Download %s" % component_name)
            base_url = "%s/%s" % (url, component["id"])
            files_list_url = "%s/dci_files_list.json" % base_url
            print("Download %s" % files_list_url)
            r = requests.get(files_list_url, cert=(cert, key))
            if r.status_code != 200:
                print(
                    "Can't get dci_files_list.json file! HTTP error code=%s, message=%s"
                    % (r.status_code, r.text)
                )
                continue
            files_list = r.json()
            if component["type"] == "Compose":
                files_list = filter_files_list(files_list, arguments)
            topic_storage_folder = os.path.join("/var/lib/dci", topic_name)
            mkdir_p(topic_storage_folder)
            if not enough_space(files_list, topic_storage_folder):
                print(
                    "Not enough space in %s/%s skipping %s"
                    % (os.getenv("LOCAL_STORAGE_FOLDER"), topic_name, component_name)
                )
                continue
            local_repo_path = os.path.join(topic_storage_folder, component_name)
            download(base_url, files_list, local_repo_path, cert, key)
    os.unlink(cert)
    os.unlink(key)
    return_code = 1 if has_error else 0
    sys.exit(return_code)


if __name__ == "__main__":
    main()

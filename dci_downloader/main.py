#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import traceback

from api import get_topic, get_components, get_keys
from cli import parse_arguments
from downloader import download_component
from fs import create_temp_file


def verify_env_variables_needed_are_setted():
    expected_env_variables = [
        "DCI_CLIENT_ID",
        "DCI_API_SECRET",
        "DCI_CS_URL",
        "LOCAL_STORAGE_FOLDER",
    ]
    for env_variable in expected_env_variables:
        if env_variable not in os.environ:
            print("Ensure %s variables are set" % ",".join(expected_env_variables))
            sys.exit(0)


def main():
    verify_env_variables_needed_are_setted()
    remoteci_id = os.getenv("DCI_CLIENT_ID").split("/")[1]
    keys = get_keys(remoteci_id)
    if keys is None:
        print("Can't get certificate's keys, contact dci administrator")
        sys.exit(0)

    arguments = parse_arguments(sys.argv[1:])
    has_error = False
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    for topic_name in arguments["topics_names"]:
        try:
            topic = get_topic(topic_name)
            if topic is None:
                has_error = True
                continue
            for component in get_components(topic):
                download_component(topic, component, arguments, cert, key)
        except Exception:
            print("Exception when downloading components for %s" % topic_name)
            traceback.print_exc()
            has_error = True
    os.unlink(cert)
    os.unlink(key)
    return_code = 1 if has_error else 0
    sys.exit(return_code)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
import traceback

from api import get_topic, get_components, get_keys
from settings import get_settings
from downloader import download_component
from fs import create_temp_file


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)


def verify_env_variables_needed_are_setted():
    expected_env_variables = [
        "DCI_CLIENT_ID",
        "DCI_API_SECRET",
        "DCI_CS_URL",
    ]
    has_error = False
    for env_variable in expected_env_variables:
        if env_variable not in os.environ:
            has_error = True
            print("Environment variable %s not set" % env_variable)
    if has_error:
        sys.exit(1)


def main():
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    verify_env_variables_needed_are_setted()
    keys = get_keys(settings["remoteci_id"])
    if keys is None:
        print("Can't get certificate's keys, contact DCI administrator")
        sys.exit(0)
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    topic_name = settings["topic_name"]
    return_code = 0
    try:
        topic = get_topic(topic_name)
        if topic is None:
            raise ("Topic name %s not found" % topic_name)
        for component in get_components(topic):
            download_component(topic, component, settings, cert, key)
    except Exception:
        print("Exception when downloading components for %s" % topic_name)
        traceback.print_exc()
        return_code = 1
    os.unlink(cert)
    os.unlink(key)
    sys.exit(return_code)


if __name__ == "__main__":
    main()

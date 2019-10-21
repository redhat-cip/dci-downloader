#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
import traceback

from dci_downloader.api import get_topic, get_components, get_keys, create_job, create_jobstate
from dci_downloader.settings import get_settings, exit_if_settings_invalid
from dci_downloader.downloader import download_component
from dci_downloader.fs import create_temp_file


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    exit_if_settings_invalid(settings)
    keys = get_keys(settings["remoteci_id"])
    if keys is None:
        print("Can't get certificate's keys, contact DCI administrator")
        sys.exit(0)
    cert = create_temp_file(keys["cert"]).name
    key = create_temp_file(keys["key"]).name
    return_code = 0

    for topic_settings in settings["topics"]:
        topic_name = topic_settings["name"]
        try:
            topic = get_topic(topic_name)
            if topic is None:
                raise ("Topic name %s not found" % topic_name)
            job = create_job(topic["id"])
            for component in get_components(topic):
                download_component(topic, component, topic_settings, cert, key)
            create_jobstate(job["id"], "download")
        except Exception:
            print("Exception when downloading components for %s" % topic_name)
            create_jobstate(job["id"], "failure")
            traceback.print_exc()
            return_code = 1
    os.unlink(cert)
    os.unlink(key)
    sys.exit(return_code)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
import traceback

from dci_downloader import api
from dci_downloader import downloader
from dci_downloader.api import (
    create_job,
    create_jobstate,
    create_tag,
)
from dci_downloader.certificates import configure_ssl_certificates
from dci_downloader.settings import get_settings, exit_if_settings_invalid


def signal_handler(sig, frame):
    print("Exiting...")
    sys.exit(130)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def download_components(settings, api, downloader):
    if "component_id" in settings and settings["component_id"]:
        component_id = settings["component_id"]
        component = api.get_component_by_id(component_id)
        topic_id = component["topic_id"]
        topic = api.get_topic_by_id(topic_id)
        components = [component]
    else:
        topic = api.get_topic(settings["name"])
        components = api.get_components(topic)
    for component in components:
        downloader.download_component(topic, component, settings)


def main():
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    exit_if_settings_invalid(settings)
    configure_ssl_certificates(settings)

    return_code = 0

    for topic_settings in settings["topics"]:
        topic_name = topic_settings["name"]
        job = None
        try:
            topic = api.get_topic(topic_name)
            if topic is None:
                raise ("Topic name %s not found" % topic_name)
            job = create_job(topic["id"])
            create_tag(job["id"], "download")
            download_components(topic_settings, api, downloader)
            create_jobstate(job["id"], "success")
        except Exception:
            print("Exception when downloading components for %s" % topic_name)
            if job is not None:
                create_jobstate(job["id"], "failure")
            traceback.print_exc()
            return_code = 1
    sys.exit(return_code)


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import functools
import os
import sys
import traceback
import time

from dci_downloader import api
from dci_downloader import downloader
from dci_downloader.lock import file_lock, LockError
from dci_downloader.fs import get_topic_folder, create_parent_dir
from dci_downloader.certificates import configure_ssl_certificates
from dci_downloader.settings import get_settings, exit_if_settings_invalid


def download_components(settings):
    if "component_id" in settings and settings["component_id"]:
        component_id = settings["component_id"]
        component = api.get_component_by_id(component_id)
        topic_id = component["topic_id"]
        topic = api.get_topic_by_id(topic_id)
        components = [component]
    else:
        topic_name = settings["name"]
        topic = api.get_topic(topic_name)
        if topic is None:
            raise Exception("Topic name %s not found" % topic_name)
        components = api.get_components(topic)
    for component in components:
        downloader.download_component(topic, component, settings)


def download_topic(settings):
    not_finished = True
    count = 0
    ten_hours = 10 * 60 * 60
    sleep = 30
    while not_finished and count < (ten_hours / sleep):
        try:
            topic_path = get_topic_folder(settings)
            lock_file = os.path.join(topic_path, ".lock")
            create_parent_dir(lock_file)
            with file_lock(lock_file):
                download_components(settings)
                not_finished = False
        except LockError:
            time.sleep(sleep)
            count += 1


def catch_all_and_print(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except KeyboardInterrupt:
            print("Keyboard interrupt exiting...")
            sys.exit(130)
        except Exception:
            traceback.print_exc()
            sys.exit(1)

    return inner


@catch_all_and_print
def main():
    api.check_repo_is_accessible()
    settings = get_settings(sys_args=sys.argv[1:], env_variables=dict(os.environ))
    exit_if_settings_invalid(settings)
    configure_ssl_certificates(settings)
    for topic_settings in settings["topics"]:
        download_topic(topic_settings)


if __name__ == "__main__":
    main()

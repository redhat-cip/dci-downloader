#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import shutil
import time

from functools import wraps

from dciclient.v1.api.context import build_signature_context
from dciclient.v1.api import topic as dci_topic
from dciclient.v1.api import remoteci as dci_remoteci


def get_topic(topic_name):
    context = build_signature_context()
    t = dci_topic.list(context, where="name:%s" % topic_name)
    t.raise_for_status()
    topics = t.json()["topics"]
    if len(topics) == 0:
        print("Ensure you have access to topic %s" % topic_name)
        print("Contact your EPM for more information.")
        return
    return topics[0]


def get_components(topic):
    context = build_signature_context()
    return context.session.post(
        "%s/jobs/schedule" % context.dci_cs_api,
        json={"topic_id": topic["id"], "dry_run": True},
    ).json()["components"]


def get_keys(remoteci_id):
    context = build_signature_context()
    remoteci = dci_remoteci.get(context, remoteci_id).json()["remoteci"]
    res = dci_remoteci.refresh_keys(context, id=remoteci_id, etag=remoteci["etag"])

    if res.status_code == 201:
        return res.json()["keys"]


def get_base_url(topic, component):
    return "https://repo.distributed-ci.io/%s/%s/%s" % (
        topic["product_id"],
        topic["id"],
        component["id"],
    )


def get_files_list(base_url, cert, key):
    print("Download DCI file list, it may take a few seconds")
    files_list_url = "%s/dci_files_list.json" % base_url
    r = requests.get(files_list_url, cert=(cert, key))
    r.raise_for_status()
    return r.json()


def retry(tries=3, delay=2, multiplier=2):
    def decorated_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            _tries = tries
            _delay = delay
            while _tries:
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    print("%s, retrying in %d seconds..." % (str(e), _delay))
                    time.sleep(_delay)
                    _tries -= 1
                    if not _tries:
                        raise
                    _delay *= multiplier
            return f(*args, **kwargs)

        return f_retry

    return decorated_retry


@retry
def download_file(file, cert, key):
    try:
        r = requests.get(file["source"], stream=True, cert=(cert, key))
        r.raise_for_status()
        with open(file["destination"], "wb") as f:
            shutil.copyfileobj(r.raw, f)
    except Exception as exc:
        print(str(exc))
        raise

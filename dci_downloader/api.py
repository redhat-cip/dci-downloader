#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import shutil
import time

from functools import wraps

from dciclient.v1.api.context import build_signature_context
from dciclient.v1.api import component as dci_component
from dciclient.v1.api import job as dci_job
from dciclient.v1.api import jobstate as dci_jobstate
from dciclient.v1.api import tag as dci_tag
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


def get_topic_by_id(topic_id):
    context = build_signature_context()
    c = dci_topic.get(context, topic_id)
    topic = c.json()["topic"]
    if len(topic) == 0:
        print("Ensure that topic %s exists or that you have access" % topic_id)
        print("Contact your EPM for more information.")
        return
    return topic


def get_component_by_id(component_id):
    context = build_signature_context()
    c = dci_component.get(context, component_id)
    component = c.json()["component"]
    if len(component) == 0:
        print("Ensure that component %s exists or that you have access" % component_id)
        print("Contact your EPM for more information.")
        return
    return component


def get_components(topic):
    context = build_signature_context()
    components = []
    for component_type in topic["component_types"]:
        res = dci_topic.list_components(
            context,
            topic["id"],
            limit=1,
            sort="-created_at",
            offset=0,
            where="type:%s,state:active" % component_type,
        ).json()
        components.extend(res["components"])
    return components


def get_keys(remoteci_id):
    context = build_signature_context()
    remoteci = dci_remoteci.get(context, remoteci_id).json()["remoteci"]
    res = dci_remoteci.refresh_keys(context, id=remoteci_id, etag=remoteci["etag"])

    if res.status_code == 201:
        return res.json()["keys"]


def create_job(topic_id):
    context = build_signature_context()
    res = dci_job.schedule(context, topic_id)

    if res.status_code == 201:
        return res.json()["job"]


def create_jobstate(job_id, status):
    context = build_signature_context()
    res = dci_jobstate.create(context, status, "download from dci-downloader", job_id)
    if res.status_code == 201:
        return res.json()["jobstate"]


def create_tag(job_id, name):
    context = build_signature_context()
    dci_tag.create(context, name)
    res = dci_job.add_tag(context, job_id, name)
    if res.status_code == 201:
        return res.json()


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


@retry()
def download_file(file, cert, key):
    r = requests.get(file["source"], stream=True, cert=(cert, key))
    r.raise_for_status()
    with open(file["destination"], "wb") as f:
        shutil.copyfileobj(r.raw, f)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import shutil
import time
import json

try:
    from urlparse import parse_qsl
    from urlparse import urlparse
    from urlparse import urljoin
except ImportError:
    from urllib.parse import parse_qsl
    from urllib.parse import urlparse
    from urllib.parse import urljoin
from functools import wraps
from dciauth.request import AuthRequest
from dciauth.signature import Signature


class Session(requests.Session):
    def __init__(self, *args, **kwargs):
        super(Session, self).__init__(*args, **kwargs)
        self.base_url = os.environ.get("DCI_CS_URL", "")
        dci_client_id = os.environ.get("DCI_CLIENT_ID", "")
        client_type, client_id = dci_client_id.split("/")[:2]
        api_secret = os.environ.get("DCI_API_SECRET", "")
        self.auth = DciSignatureAuth(client_type, client_id, api_secret)

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.base_url, url)
        return super(Session, self).request(method, url, *args, **kwargs)


class DciSignatureAuth(requests.auth.AuthBase):
    def __init__(self, client_type, client_id, api_secret):
        self.client_type = client_type
        self.client_id = client_id
        self.api_secret = api_secret

    def __call__(self, r):
        url = urlparse(r.url)
        params = dict(parse_qsl(url.query))
        payload = self.get_payload(r)
        request = AuthRequest(
            method=r.method,
            endpoint=url.path,
            headers=r.headers,
            params=params,
            payload=payload,
        )
        headers = Signature(request).generate_headers(
            client_type=self.client_type,
            client_id=self.client_id,
            secret=self.api_secret,
        )
        r.headers.update(headers)
        return r

    def get_payload(self, r):
        try:
            body = r.body.decode("utf-8")
        except AttributeError:
            body = r.body
        return dict(json.loads(body or "{}"))


def get_topic(topic_name):
    with Session() as s:
        params = {"where": "name:%s" % topic_name}
        response = s.get("/api/v1/topics", params=params)
        response.raise_for_status()
        topics = response.json()["topics"]
        if len(topics) == 0:
            print("Ensure you have access to topic %s" % topic_name)
            print("Contact your EPM for more information.")
            return
        return topics[0]


def get_topic_by_id(topic_id):
    with Session() as s:
        response = s.get("/api/v1/topics/%s" % topic_id)
        response.raise_for_status()
        topic = response.json()["topic"]
        if len(topic) == 0:
            print("Ensure that topic %s exists or that you have access" % topic_id)
            print("Contact your EPM for more information.")
            return
        return topic


def get_component_by_id(component_id):
    with Session() as s:
        response = s.get("/api/v1/components/%s" % component_id)
        response.raise_for_status()
        component = response.json()["component"]
        if len(component) == 0:
            print(
                "Ensure that component %s exists or that you have access" % component_id
            )
            print("Contact your EPM for more information.")
            return
        return component


def get_components(topic):
    components = []
    with Session() as s:
        for component_type in topic["component_types"]:
            params = {
                "sort": "-created_at",
                "offset": 0,
                "where": "type:%s,state:active" % component_type,
            }
            response = s.get(
                "/api/v1/topics/%s/components" % topic["id"], params=params
            )
            response.raise_for_status()
            components.extend(response.json()["components"])
        return components


def get_remoteci_by_id(remoteci_id):
    with Session() as s:
        response = s.get("/api/v1/remotecis/%s" % remoteci_id)
        response.raise_for_status()
        remoteci = response.json()["remoteci"]
        return remoteci


def get_keys(remoteci_id):
    with Session() as s:
        remoteci = get_remoteci_by_id(remoteci_id)
        headers = {"If-match": remoteci["etag"]}
        response = s.put("/api/v1/remotecis/keys", headers=headers)
        response.raise_for_status()
        return response.json()["keys"]


def create_job(topic_id):
    with Session() as s:
        response = s.post("/api/v1/jobs", json={"topic_id": topic_id})
        response.raise_for_status()
        return response.json()["job"]


def create_jobstate(job_id, status):
    with Session() as s:
        response = s.post(
            "/api/v1/jobstates",
            json={
                "job_id": job_id,
                "status": status,
                "comment": "download from dci-downloader",
            },
        )
        response.raise_for_status()
        return response.json()["jobstate"]


def create_tag(job_id, name):
    with Session() as s:
        response = s.post("/api/v1/jobs/%s/tags" % job_id, json={"name": name},)
        response.raise_for_status()
        return response.json()


def get_repo_base_url(topic, component):
    return "https://repo.distributed-ci.io/%s/%s/%s" % (
        topic["product_id"],
        topic["id"],
        component["id"],
    )


def get_files_list(base_url, cert, key):
    print("Download DCI file list, it may take a few seconds")
    files_list_url = "%s/dci_files_list.json" % base_url
    response = requests.get(files_list_url, cert=(cert, key))
    response.raise_for_status()
    return response.json()


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

FROM centos:7

LABEL name="dci-downloader"
LABEL version="0.1.0"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8

RUN yum upgrade -y && \
  yum -y install epel-release https://packages.distributed-ci.io/dci-release.el7.noarch.rpm && \
  yum -y install gcc ansible python python2-devel python2-pip ansible-role-dci-import-keys ansible-role-dci-retrieve-component dci-ansible && \
  yum clean all

ADD requirements.txt /usr/share/dci-downloader/requirements.txt
RUN pip install --upgrade pip
RUN pip install --requirement /usr/share/dci-downloader/requirements.txt

ADD dci_downloader /usr/share/dci-downloader/

# Ansible-runner bug: https://github.com/ansible/ansible-runner/issues/219
RUN cp /usr/share/dci/callback/dci.py /usr/lib/python2.7/site-packages/ansible_runner/callbacks

WORKDIR /usr/share/dci-downloader

ENTRYPOINT ["python", "download.py"]

CMD []
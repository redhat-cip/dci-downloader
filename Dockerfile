FROM centos:7

LABEL name="dci-downloader"
LABEL version="0.1.0"
LABEL maintainer="DCI Team <distributed-ci@redhat.com>"

ENV LANG en_US.UTF-8

RUN yum upgrade -y && \
  yum -y install python python2-pip && \
  yum clean all

ADD requirements.txt /usr/share/dci-downloader/requirements.txt
RUN pip install --upgrade pip
RUN pip install --requirement /usr/share/dci-downloader/requirements.txt

ADD dci_downloader /usr/share/dci-downloader/


WORKDIR /usr/share/dci-downloader

ENTRYPOINT ["python", "download.py"]

CMD []
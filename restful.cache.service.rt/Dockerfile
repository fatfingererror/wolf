
FROM ubuntu:trusty

# Environment
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV PROJECT_NAME restful.cache.service.rt
ENV PROJECT_ROOT /srv/$PROJECT_NAME

WORKDIR $PROJECT_ROOT
RUN mkdir log

ADD ./restful.cache.service.rt $PROJECT_ROOT

RUN apt-get update --fix-missing
RUN apt-get install -y build-essential python3.4 python3-pip python3-dev libffi-dev libssl-dev

# Set "en_US.UTF-8" locale as default
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN pip3 install --upgrade pip && pip install --no-cache-dir --upgrade --force-reinstall -r requirements.txt

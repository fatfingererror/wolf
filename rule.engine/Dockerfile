FROM ubuntu:trusty

# RUN mkdir /code

# ADD run_rest_api_tests.sh /code/
# ADD data /code/data
# ADD autogrid_integration /code/autogrid_integration
# ADD domain_model /code/domain_model
# ADD handlers /code/handlers
# ADD integration /code/integration
# ADD repositories /code/repositories
# ADD scripts /code/scripts
# ADD rest_api /code/rest_api
# WORKDIR /code
# RUN pip install -r /code/rest_api/requirements/prod.txt

# ADD . /srv/rule_engine

# WORKDIR /code/rest_api

# Environment
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8
ENV PROJECT_NAME rule.engine
ENV PROJECT_ROOT /srv/$PROJECT_NAME

ADD bin $PROJECT_ROOT/bin
ADD pom.xml $PROJECT_ROOT/pom.xml

WORKDIR $PROJECT_ROOT

# # Update box
RUN \
    apt-get update && \
    apt-get upgrade -y --force-yes && \
    apt-get install -y --force-yes git maven2 && \
    apt-get install -y --force-yes openjdk-7-jdk zookeeper
#     apt-get install -y --force-yes python3.4=3.4.0-2ubuntu1.1  && \
#     apt-get install -y --force-yes python3.4-minimal=3.4.0-2ubuntu1.1 && \
#     apt-get install -y --force-yes libpython3.4-stdlib=3.4.0-2ubuntu1.1 && \
#     apt-get install -y --force-yes libpython3.4-minimal=3.4.0-2ubuntu1.1 && \
#     apt-get install -y --force-yes python3-pip python3-dev && \
#     apt-get install -y --force-yes libpq-dev libpq5 libxml2 libxml2-dev libxslt1-dev libffi-dev libssl-dev

# Cleanup box
RUN \
    apt-get autoclean -y --force-yes && \
    apt-get clean -y --force-yes && \
    apt-get autoremove -y --force-yes  && \
    apt-get purge -y --force-yes  && \
    rm -rf /var/lib/apt/lists/*

# # Set "en_US.UTF-8" locale as default
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

RUN mvn clean install

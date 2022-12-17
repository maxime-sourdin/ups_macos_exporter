FROM proxy-docker.sourdin.ovh/python:3.8.16-alpine3.17
WORKDIR /worker/
USER root
RUN apk update \
    && apk upgrade \
    && apk --no-cache add bash py3-pip shadow\
    && useradd -m worker \
    && chown -R worker:worker /worker
USER 1000
COPY --chown=worker:worker ups.py /worker/ups.py
COPY --chown=worker:worker requirements.txt /worker/requirements.txt
ENV PATH $PATH:$HOME/.local/bin
RUN pip3 install -r requirements.txt
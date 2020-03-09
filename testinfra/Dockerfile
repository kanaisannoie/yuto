FROM alpine:3.9

RUN apk update && \
apk add python3 python3-dev gcc libffi-dev libtool musl-dev openssl-dev openssh make
#apk add python3 python3-dev gcc libtool musl-dev libffi-dev openssl-dev py3-pynacl openssh

WORKDIR /testinfra
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt



FROM alpine:3.9

RUN apk update && \
apk add python3 python3-dev gcc libtool musl-dev libffi-dev openssl-dev py3-pynacl openssh

WORKDIR /ansible
COPY ./requirements.txt .
RUN pip install -r requirements.txt

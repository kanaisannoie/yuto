#!/bin/sh
docker run -d -p 5000:5000 -v /var/opt/docker-registry:/var/lib/registry registry:2.3.0

#!/bin/sh
docker build -t dict-python -f Dockerfile.python .
docker build -t dict-python-admin -f Dockerfile.python-admin .
docker build -t dict-nginx -f Dockerfile.nginx .
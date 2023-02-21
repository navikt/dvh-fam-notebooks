#!/bin/sh
set -e

echo "Specify a new version number (example. 1.2.1):"
read version

echo "Authenticate to GitHub container registry (ghcr.io)"
docker login ghcr.io

docker build . -t ghcr.io/navikt/dvh-python-libraries:$version
docker push ghcr.io/navikt/dvh-python-libraries:$version

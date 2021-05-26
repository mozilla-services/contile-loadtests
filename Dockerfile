# Mozilla Contile Load-Tester

FROM python:3-slim

RUN mkdir -p /app
ADD . /app
WORKDIR /app

# Building:
# you can build a local docker image using
# `docker build . --tag contile-loadtest:local`

# system setup
RUN \
    BUILD_DEPS="git build-essential" && \
    # wget not required but nice to have
    RUN_DEPS="wget libssl-dev" && \
    apt-get update && \
    apt-get install -yq --no-install-recommends ${BUILD_DEPS} ${RUN_DEPS} && \
    pip install virtualenv && \
    python -m virtualenv -p `which python` apenv

# app install
RUN \
    ./apenv/bin/pip install -r requirements.txt && \
    apt-get purge -yq --auto-remove ${BUILD_DEPS} && \
    apt-get autoremove -yqq && \
    apt-get clean -y

# Using:
# Start an interactive terminal using
# `docker run --net=host -it contile-loadtest:local`
# This will start a bash shell as root.
# You can fire off a load test by calling:
# `TARGET_URL=http://<Contile host>/v1/tiles TEST_LOCATION_HEADER_NAME=x-test-location TIMEOUT=5 ./apenv/bin/molotov -v -s <scenario name>`
#
# NOTE: TEST_LOCATION_HEADER_NAME should match the value of CONTILE_LOCATION_TEST_HEADER on Contile

ENTRYPOINT ["/bin/bash"]

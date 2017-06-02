# Dockerfile for testing the full vim plugin
FROM buildpack-deps:xenial

RUN apt-get update && apt-get install -y --no-install-recommends \
    python-dev \
    vim-nox-py2

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

RUN pip install --no-cache-dir \
    google-api-python-client \
    Cython \
    py-stackexchange \
    lxml

WORKDIR /gso

COPY . .

RUN python setup.py install

WORKDIR /workspace

CMD ["/bin/bash"]

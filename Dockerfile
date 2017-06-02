FROM mcranmer/dockers:dev

RUN pip install google-api-python-client

WORKDIR /workspace

RUN ["/bin/zsh"]

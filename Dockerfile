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

# Install Vundle with GSO
RUN git clone --depth=1 https://github.com/VundleVim/Vundle.vim.git $HOME/.vim/bundle/Vundle.vim && \
    wget https://raw.githubusercontent.com/VundleVim/Vundle.vim/11fdc428fe741f4f6974624ad76ab7c2b503b73e/test/minirc.vim -O $HOME/.vimrc && \
    sed -i "7i Plugin 'file:///gso/'" $HOME/.vimrc && \
    vim +PluginInstall +qall


WORKDIR /workspace

CMD ["/bin/bash"]

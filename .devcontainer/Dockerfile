FROM mcr.microsoft.com/devcontainers/anaconda:0-3

RUN mkdir -p /workspaces

RUN cd /workspaces/ \
    && git clone https://github.com/dwest77a/tdl_manager \
    && cd tdl_manager/ \
    && pip install -r requirements.txt

RUN git config --system --add safe.directory /workspaces/tdl_manager

RUN chown -R vscode:vscode /workspaces/tdl_manager

RUN if ["true" = "true"]; then echo 'RUNNING TRUE'; fi

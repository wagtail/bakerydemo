FROM gitpod/workspace-full
ENV PYTHONUSERBASE=/workspace/.pip-modules
ENV PATH=$PYTHONUSERBASE/bin:$PATH
ENV PIP_USER=yes

FROM        python:3.8.12-slim

ENV         LANG C.UTF-8
ENV         USER app
ENV         PROJECTPATH=/home/app/

ENV         PYTHONFAULTHANDLER=1 \
            PYTHONHASHSEED=random \
            PYTHONUNBUFFERED=1

WORKDIR     ${PROJECTPATH}

RUN         set -x \
            && apt-get -qq update \
            && apt-get install -y --no-install-recommends \
               build-essential libpq-dev git gettext binutils curl \
            && apt-get purge -y --auto-remove \
            && rm -rf /var/lib/apt/lists/*

ADD         https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait ${PROJECTPATH}/wait
RUN         chmod +x ${PROJECTPATH}/wait

RUN         pip install --upgrade pip \
            && pip install -U pytest celery

RUN         useradd -m -d /home/${USER} ${USER} \
            && mkdir -p /home/${USER}/logs/ \
            && chown -R ${USER} /home/${USER}

RUN         pip3 install poetry

COPY        pyproject.toml ${PROJECTPATH}/

RUN         poetry config virtualenvs.create false

RUN         poetry install --no-dev
RUN         poetry add platformdirs

COPY        . ${PROJECTPATH}

USER         ${user}

EXPOSE      8000

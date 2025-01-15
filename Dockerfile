FROM apache/airflow:2.10.2

USER root

ENV POETRY_VERSION=1.8.4 

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        vim \
        nano \
        curl && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

USER airflow

RUN pip install --no-cache-dir --upgrade pip 

RUN pip install pipx && \
    pipx install poetry==${POETRY_VERSION}

RUN poetry config virtualenvs.in-project false && \
    poetry export --without-hashes --format=requirements.txt > /opt/airflow/requirements.txt

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

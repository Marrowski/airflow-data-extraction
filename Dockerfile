ARG AIRFLOW_VERSION=3.3.0
ARG PYTHON_VERSION=3.13

FROM apache/airflow:${AIRFLOW_VERSION}-python${PYTHON_VERSION}

ENV AIRFLOW_HOME=/opt/airflow
COPY requirements.txt /

RUN pip install --no-cache "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt && \
    pip install --no-cache --no-deps soda-core-postgres==3.3.14 soda-core==3.3.14 && \
    pip install --no-cache "ruamel.yaml>=0.16.0,<0.18.8" "antlr4-python3-runtime==4.11.1"
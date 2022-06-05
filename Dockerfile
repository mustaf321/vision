FROM python:3.9

EXPOSE 8080
WORKDIR /usr/src/

COPY ./src .
ENV DOCKER_INFLUXDB_INIT_ORG=my \
    DOCKER_INFLUXDB_INIT_BUCKET=my\
    DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

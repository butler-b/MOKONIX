FROM mariadb:latest

RUN apt-get update && \
    apt-get install -y sudo python3 vim wget gnupg

COPY init.sql /docker-entrypoint-initdb.d/


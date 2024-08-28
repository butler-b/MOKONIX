FROM nginx:latest

RUN apt-get update && \
    apt-get install -y sudo python3 vim wget gnupg

COPY nginx.conf /etc/nginx/nginx.conf


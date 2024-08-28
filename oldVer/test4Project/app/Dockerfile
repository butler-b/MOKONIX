FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y sudo python3 vim wget gnupg pkg-config libmariadb-dev gcc

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]


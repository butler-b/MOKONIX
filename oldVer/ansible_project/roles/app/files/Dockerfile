FROM python:3.9-slim

# 기본 패키지 및 의존성 설치
RUN apt-get update && \
    apt-get install -y sudo python3 vim wget gnupg pkg-config libmariadb-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 복사 및 의존성 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir prometheus_client

# 애플리케이션 소스 코드 복사
COPY . .

# Flask 애플리케이션 실행 명령어
CMD ["flask", "run", "--host=0.0.0.0"]


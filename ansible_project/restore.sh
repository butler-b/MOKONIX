#!/bin/bash

# 복원할 날짜를 입력받음
DATE=$1

if [ -z "$DATE" ]; then
  echo "Usage: $0 <backup-date>"
  exit 1
fi

# ElasticSearch 데이터 복원
echo "Restoring ElasticSearch data..."
docker exec -t elasticsearch /usr/share/elasticsearch/bin/elasticsearch-snapshot.sh /backup/elastic-${DATE}.tar.gz --restore

# Prometheus 데이터 복원
echo "Restoring Prometheus data..."
docker exec -t prometheus tar xzvf /backup/prometheus-${DATE}.tar.gz -C /prometheus

# 복원 완료 메시지
echo "Restore completed successfully."

#!/bin/bash

# 날짜 형식 지정
DATE=$(date +%Y%m%d%H%M)

# ElasticSearch 데이터 백업
echo "Starting ElasticSearch backup..."
docker exec -t elasticsearch /usr/share/elasticsearch/bin/elasticsearch-snapshot.sh /backup/elastic-${DATE}.tar.gz

# Prometheus 데이터 백업
echo "Starting Prometheus backup..."
docker exec -t prometheus tar czvf /backup/prometheus-${DATE}.tar.gz /prometheus

# 백업 완료 메시지
echo "Backup completed successfully."

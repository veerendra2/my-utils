#!/usr/bin/env bash

# Set Elasticsearch host, username, and password
ES_HOST=""
ES_USER="elastic"
ES_PASS=""

# Get the current date and calculate the date three months ago
CURRENT_DATE=$(date +%Y.%m.%d)
THREE_MONTHS_AGO=$(date -v -2m +%Y.%m.%d)

# List all indices and filter by date format "test-report-YYYY.MM.DD"
INDICES=$(curl -s -u $ES_USER:$ES_PASS "$ES_HOST/_cat/indices?h=index" | grep -E '^test-report-[0-9]{4}\.[0-9]{2}\.[0-9]{2}$')

# Loop through each index and delete if it's older than three months
for INDEX in $INDICES; do
  # Extract the date part of the index name
  INDEX_DATE=$(echo $INDEX | sed -E 's/test-report-([0-9]{4}\.[0-9]{2}\.[0-9]{2})/\1/')

  # Compare index date with three months ago date
  if [[ "$INDEX_DATE" < "$THREE_MONTHS_AGO" ]]; then
    echo "index: $INDEX"
    curl -X DELETE -u $ES_USER:$ES_PASS "$ES_HOST/$INDEX"
  fi
done


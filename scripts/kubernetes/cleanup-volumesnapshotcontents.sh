#!/usr/bin/env bash

DAYS=31

CURRENT_DATE=$(date +%s)

kubectl get volumesnapshotcontent --all-namespaces -o json | jq -c '.items[] | {name: .metadata.name, creationTimestamp: .metadata.creationTimestamp}' | while read -r snapshot_content; do
  NAME=$(echo "$snapshot_content" | jq -r '.name')
  CREATION_TIMESTAMP=$(echo "$snapshot_content" | jq -r '.creationTimestamp')
  CREATION_DATE=$(date -jf "%Y-%m-%dT%H:%M:%SZ" "$CREATION_TIMESTAMP" +%s)
  AGE=$(( (CURRENT_DATE - CREATION_DATE) / 86400 ))

  if [ "$AGE" -gt "$DAYS" ]; then
    HUMAN_READABLE_DATE=$(date -jf "%Y-%m-%dT%H:%M:%SZ" "$CREATION_TIMESTAMP" +"%Y-%m-%d %H:%M:%S UTC")
    sleep 1
    echo "VolumeSnapshotContent: $NAME (age: $AGE days, created: $HUMAN_READABLE_DATE)"
    kubectl delete volumesnapshotcontent "$NAME" &
    sleep 10
    pkill -f "kubectl delete volumesnapshot"
    kubectl patch volumesnapshotcontent/$NAME --type json --patch='[ { "op": "remove", "path": "/metadata/finalizers" } ]'
  fi
done

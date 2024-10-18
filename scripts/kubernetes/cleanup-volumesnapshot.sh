#!/usr/bin/env bash

DAYS=31

CURRENT_DATE=$(date +%s)

kubectl get volumesnapshot --all-namespaces -o json | jq -c '.items[] | {name: .metadata.name, namespace: .metadata.namespace, creationTimestamp: .metadata.creationTimestamp}' | while read -r snapshot; do
  NAME=$(echo "$snapshot" | jq -r '.name')
  NAMESPACE=$(echo "$snapshot" | jq -r '.namespace')
  CREATION_TIMESTAMP=$(echo "$snapshot" | jq -r '.creationTimestamp')
  CREATION_DATE=$(date -jf "%Y-%m-%dT%H:%M:%SZ" "$CREATION_TIMESTAMP" +%s)
  AGE=$(( (CURRENT_DATE - CREATION_DATE) / 86400 ))

  if [ "$AGE" -gt "$DAYS" ]; then
    HUMAN_READABLE_DATE=$(date -jf "%Y-%m-%dT%H:%M:%SZ" "$CREATION_TIMESTAMP" +"%Y-%m-%d %H:%M:%S UTC")

    echo "VolumeSnapshot: $NAME in namespace: $NAMESPACE (age: $AGE days, created: $HUMAN_READABLE_DATE)"
    kubectl delete volumesnapshot "$NAME" -n "$NAMESPACE"
  fi
done

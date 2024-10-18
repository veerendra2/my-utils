#!/usr/bin/env bash

echo "Checking for orphaned VolumeSnapshotContents..."

kubectl get volumesnapshotcontent -o json | jq -c '.items[]' | while read -r vsc; do
  snapshot_name=$(echo "$vsc" | jq -r '.spec.volumeSnapshotRef.name')
  snapshot_namespace=$(echo "$vsc" | jq -r '.spec.volumeSnapshotRef.namespace')
  vsc_name=$(echo "$vsc" | jq -r '.metadata.name')

  snapshot_exists=$(kubectl get volumesnapshot "$snapshot_name" -n "$snapshot_namespace" --ignore-not-found)

  if [[ -z "$snapshot_exists" ]]; then
    echo "Orphaned VolumeSnapshotContent found: $vsc_name (linked to non-existent VolumeSnapshot: $snapshot_name in namespace: $snapshot_namespace)"
  fi
done

#!/usr/bin/env bash
#
# A simple backup script using restic and rclone
#
# Rclone google drive config: https://rclone.org/drive/#making-your-own-client-id
# Restic rclone config: https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#other-services-via-rclone

RCLONE_CONFIG="google-drive"
RESTIC_REPO="my-home-backup"
BACKUP_SRC="/Users/veerendra"

restic -r rclone:${RCLONE_CONFIG}:${RESTIC_REPO} backup ${BACKUP_SRC} \
  --exclude Applications \
  --exclude Library \
  --exclude "VirtualBox VMs" \
  --exclude Public \
  --exclude Pictures \
  --exclude Movies \
  --exclude *minikube* \
  --exclude .DS_Store \
  --exclude .Trash \
  --exclude .cache \
  --exclude .vagrant* \
  --exclude Postman \
  --password-file /opt/restic/pass.txt \
  --json

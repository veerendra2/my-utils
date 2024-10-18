#!/usr/bin/env bash
#
# Rclone google drive config: https://rclone.org/drive/#making-your-own-client-id
# Restic rclone config: https://restic.readthedocs.io/en/latest/030_preparing_a_new_repo.html#other-services-via-rclone

RCLONE_CONFIG="google-drive"
RESTIC_REPO="my-home-backup"
BACKUP_SRC="/Users/veerendra.kakumanu"

echo [$(/bin/date '+%d-%m-%Y %H:%M:%S')] start resitic backup

restic -r rclone:${RCLONE_CONFIG}:${RESTIC_REPO} backup ${BACKUP_SRC} \
  --exclude ${BACKUP_SRC}/Applications \
  --exclude ${BACKUP_SRC}/Library \
  --exclude ${BACKUP_SRC}/"VirtualBox VMs" \
  --exclude ${BACKUP_SRC}/Public \
  --exclude ${BACKUP_SRC}/Pictures \
  --exclude ${BACKUP_SRC}/Movies \
  --exclude ${BACKUP_SRC}/Postman \
  --exclude ${BACKUP_SRC}/.minikube \
  --exclude ${BACKUP_SRC}/.DS_Store \
  --exclude ${BACKUP_SRC}/.Trash \
  --exclude ${BACKUP_SRC}/.cache \
  --exclude ${BACKUP_SRC}/.vagrant*/ \
  --exclude ${BACKUP_SRC}/.npm \
  --exclude ${BACKUP_SRC}/.pub-cache \
  --exclude ${BACKUP_SRC}/.vscode \
  --exclude ${BACKUP_SRC}/.vs-kubernetes \
  --exclude ${BACKUP_SRC}/backups \
  --exclude ${BACKUP_SRC}/development \
  --exclude ${BACKUP_SRC}/go \
  --exclude ${BACKUP_SRC}/.ansible \
  --exclude ${BACKUP_SRC}/.orbstack \
  --password-file /opt/restic/pass.txt \
  --json

echo [$(/bin/date '+%d-%m-%Y %H:%M:%S')] end resitic backup

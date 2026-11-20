#!/usr/bin/env bash
# Script: backup.sh
# Description: Creates an encrypted Restic backup of Homelab data and files.
# Usage: sudo RESTIC_REPOSITORY=/mnt/homelab-backup/restic \
#        RESTIC_PASSWORD_FILE=/root/.config/restic/password ./backup.sh
# Requirements: External backup disk mounted; repository initialized; password file protected.
# Notes: Does not back up live PostgreSQL data consistently; dump databases first.

set -Eeuo pipefail
source "$(dirname "$0")/../lib/common.sh"
require_root
: "${RESTIC_REPOSITORY:?Set RESTIC_REPOSITORY}"
: "${RESTIC_PASSWORD_FILE:?Set RESTIC_PASSWORD_FILE}"
[[ -d /srv/homelab/data ]] || die "/srv/homelab/data does not exist"
[[ -d /srv/homelab/files ]] || die "/srv/homelab/files does not exist"
[[ -f "$RESTIC_PASSWORD_FILE" ]] || die "Restic password file not found"
[[ -d "$(dirname "$RESTIC_REPOSITORY")" ]] || die "Backup destination is not mounted"

export RESTIC_REPOSITORY RESTIC_PASSWORD_FILE
restic backup /srv/homelab/data /srv/homelab/files
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune
log "Backup and retention completed."

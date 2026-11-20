#!/usr/bin/env bash
# Script: restore.sh
# Description: Restores a Restic snapshot into a target directory.
# Usage: sudo RESTIC_REPOSITORY=... RESTIC_PASSWORD_FILE=... ./restore.sh SNAPSHOT_ID TARGET_DIR
# Safety: Restore to a temporary directory first. This script refuses / and /srv/homelab.

set -Eeuo pipefail
source "$(dirname "$0")/../lib/common.sh"
require_root
[[ $# -eq 2 ]] || die "Usage: $0 SNAPSHOT_ID TARGET_DIR"
: "${RESTIC_REPOSITORY:?Set RESTIC_REPOSITORY}"
: "${RESTIC_PASSWORD_FILE:?Set RESTIC_PASSWORD_FILE}"
SNAPSHOT="$1"
TARGET="$(realpath -m "$2")"
[[ "$TARGET" != "/" && "$TARGET" != "/srv/homelab" ]] || die "Unsafe restore target"
[[ "$TARGET" == /tmp/* || "$TARGET" == /mnt/* ]] || die "Use a temporary or mounted restore directory"
export RESTIC_REPOSITORY RESTIC_PASSWORD_FILE
install -d -m 0700 "$TARGET"
restic restore "$SNAPSHOT" --target "$TARGET"
log "Restore completed into $TARGET. Inspect before replacing live data."

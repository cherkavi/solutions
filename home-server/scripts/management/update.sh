#!/usr/bin/env bash
# Script: update.sh
# Description: Updates Ubuntu packages after confirmation.
# Usage: sudo ./scripts/management/update.sh
# Notes: Docker image updates are separate and always manual via homelab.sh pull/up.

set -Eeuo pipefail
source "$(dirname "$0")/../lib/common.sh"
require_root
read -r -p "Update Ubuntu packages now? [y/N] " answer
[[ "$answer" =~ ^[Yy]$ ]] || { log "Cancelled."; exit 0; }
apt-get update
apt-get full-upgrade
log "OS package update completed. Reboot if required."

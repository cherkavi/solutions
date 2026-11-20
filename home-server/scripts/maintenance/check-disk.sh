#!/usr/bin/env bash
# Script: check-disk.sh
# Description: Shows filesystem usage and disk health information.
# Usage: ./scripts/maintenance/check-disk.sh
# Notes: SMART/NVMe commands may require sudo and device-specific options.

set -Eeuo pipefail
df -hT
echo
lsblk -o NAME,MODEL,SIZE,TYPE,FSTYPE,MOUNTPOINTS
echo
sudo smartctl --scan 2>/dev/null || true

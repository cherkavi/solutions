#!/usr/bin/env bash
# Script: check-memory.sh
# Description: Shows memory and top memory-consuming processes/containers.
# Usage: ./scripts/maintenance/check-memory.sh

set -Eeuo pipefail
free -h
echo
ps aux --sort=-%mem | head -n 12
echo
docker stats --no-stream 2>/dev/null || true

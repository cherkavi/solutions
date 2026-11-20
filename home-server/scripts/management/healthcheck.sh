#!/usr/bin/env bash
# Script: healthcheck.sh
# Description: Prints host, storage, Docker and container resource health.
# Usage: ./scripts/management/healthcheck.sh

set -Eeuo pipefail
echo "=== Host ==="
hostnamectl
echo
echo "=== Memory ==="
free -h
echo
echo "=== Filesystems ==="
df -hT
echo
echo "=== Docker ==="
docker info --format 'Docker={{.ServerVersion}} StorageDriver={{.Driver}}' 2>/dev/null || true
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
echo
echo "=== Resource usage ==="
docker stats --no-stream 2>/dev/null || true
echo
echo "=== Zigbee USB devices ==="
ls -l /dev/serial/by-id/ 2>/dev/null || true

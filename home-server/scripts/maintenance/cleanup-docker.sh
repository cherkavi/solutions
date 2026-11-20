#!/usr/bin/env bash
# Script: cleanup-docker.sh
# Description: Removes dangling Docker images and build cache after confirmation.
# Usage: sudo ./scripts/maintenance/cleanup-docker.sh
# Safety: Does not remove volumes or all unused images.

set -Eeuo pipefail
read -r -p "Remove dangling images and build cache? [y/N] " answer
[[ "$answer" =~ ^[Yy]$ ]] || exit 0
docker image prune
docker builder prune

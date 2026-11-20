#!/usr/bin/env bash
# 
# Description: Remote access to the server without exposing IP address in the public internet. Installs Tailscale on the Ubuntu host for resilient remote administration.
#
# Usage: sudo ./scripts/install/03-install-tailscale.sh
# Security: Never commit an auth key or generated credentials to Git.

set -Eeuo pipefail
source "$(dirname "$0")/../lib/common.sh"
require_root

curl -fsSL https://tailscale.com/install.sh | sh
systemctl enable --now tailscaled
log "Tailscale installed. Authenticate with: sudo tailscale up"

sudo tailscale up
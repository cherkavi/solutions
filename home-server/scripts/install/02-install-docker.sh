#!/usr/bin/env bash
# Script: 02-install-docker.sh
# Description: Installs Docker Engine and Compose V2 from Docker's official apt repository.
# Usage: sudo ./scripts/install/02-install-docker.sh
# Supports: Ubuntu releases listed by Docker's official documentation.
# Security: Docker group membership is effectively root access; this script does not add users.

set -Eeuo pipefail
source "$(dirname "$0")/../lib/common.sh"
require_root

. /etc/os-release
[[ "${ID:-}" == "ubuntu" ]] || die "This installer supports Ubuntu only."
ARCH="$(dpkg --print-architecture)"
CODENAME="${UBUNTU_CODENAME:-${VERSION_CODENAME:-}}"
[[ -n "$CODENAME" ]] || die "Cannot determine Ubuntu codename."

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y ca-certificates curl

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

cat >/etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: ${CODENAME}
Components: stable
Architectures: ${ARCH}
Signed-By: /etc/apt/keyrings/docker.asc
EOF

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable --now docker
docker run --rm hello-world
docker compose version
log "Docker Engine and Compose V2 installed."
log "For convenience, you may add your user to docker group, but that grants root-equivalent privileges."

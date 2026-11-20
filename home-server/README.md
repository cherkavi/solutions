# homelab-ubuntu

home-server project for Ubuntu Server, Docker Compose, Zigbee2MQTT, Home Assistant, storage, monitoring, development services and optional local AI.

## Target hardware
- Intel Core i3/i5 (exact generation unknown)
- 8 GB RAM
- 512 GB SSD
- Wi-Fi networking
- Zigbee USB coordinator (example: Sonoff ZBDongle-P)

## Design principles

1. Ubuntu Server is the host OS; Docker Compose runs application services.
2. Host-critical services (networking, SSH, Tailscale, firewall, Restic scheduling) remain on Ubuntu.
3. Each application group has an independent Compose project.
4. Deployment and updates are manual. Nothing in this repository automatically deploys from GitHub.
5. Secrets and personal data never belong in this public repository.
6. Persistent application data lives under `/srv/homelab/data`, outside the Git checkout.
7. Backups must be stored on a separate disk and ideally copied off-site.

## Supported OS

The scripts target Ubuntu Server 26.04 LTS (amd64). Docker's official Ubuntu installation documentation currently lists Ubuntu 26.04 LTS as supported. If you choose Ubuntu 24.04 LTS instead, the Docker repository setup script detects the installed codename automatically.

## Quick start

Read `docs/installation.md` before executing anything.

```bash
git clone https://github.com/YOUR_GITHUB_USER/homelab-ubuntu.git
cd homelab-ubuntu

cp .env.example .env
chmod 600 .env

# Review and edit .env, especially the Zigbee USB path.
nano .env

# Install host prerequisites and Docker (review scripts first).
sudo ./scripts/install/01-system-setup.sh
sudo ./scripts/install/02-install-docker.sh
sudo ./scripts/install/03-install-tailscale.sh

# Create persistent directories.
sudo ./scripts/install/04-setup-storage.sh

# Start selected projects.
./scripts/management/homelab.sh up smart-home
./scripts/management/homelab.sh status
```

Do not run every project at once on an 8 GB machine. Start with `smart-home`, `storage`, and `monitoring`. Start `development` and `ai` only when needed.

## Repository layout

```text
.
├── README.md
├── .env.example
├── .gitignore
├── compose/
│   ├── smart-home/
│   ├── storage/
│   ├── monitoring/
│   ├── infrastructure/
│   ├── development/
│   └── ai/
├── config/
│   ├── mosquitto/
│   └── zigbee2mqtt/
├── docs/
└── scripts/
    ├── install/
    ├── management/
    └── maintenance/
```

## Management commands

```bash
./scripts/management/homelab.sh list
./scripts/management/homelab.sh status
./scripts/management/homelab.sh up smart-home
./scripts/management/homelab.sh down smart-home
./scripts/management/homelab.sh restart monitoring
./scripts/management/homelab.sh logs smart-home
./scripts/management/homelab.sh pull smart-home
./scripts/management/homelab.sh config smart-home
```

The `pull` command only downloads images. It does not recreate running containers. To apply image updates, explicitly run `up` after reviewing the changes and taking backups.

## Important safety notes

- Docker-published ports can bypass ordinary UFW rules. Review `docs/security.md` before exposing services.
- Do not publish MQTT, PostgreSQL, Qdrant, Ollama, or administration interfaces to the public Internet.
- The Docker `group` grants root-equivalent privileges. Understand this before adding a user to it.
- Do not store `.env`, MQTT password files, Tailscale auth keys, SSH private keys, Home Assistant secrets, Zigbee network keys, or backups in Git.
- Keep the Zigbee coordinator on a USB extension cable and use `/dev/serial/by-id/...` on the host.
- Home Assistant Container does not include Home Assistant OS Supervisor or add-on management.
- Restic backups are not a substitute for testing restores.

## Documentation

- [Architecture](docs/architecture.md)
- [Installation](docs/installation.md)
- [Networking](docs/networking.md)
- [Security](docs/security.md)
- [Services](docs/services.md)
- [Backup and recovery](docs/backup-and-recovery.md)
- [Operations runbook](docs/operations.md)\n- [Publish to GitHub](docs/github-publication.md)

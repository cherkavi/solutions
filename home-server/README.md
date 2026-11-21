# homelab-ubuntu
home server with:
* Zigbee2MQTT
* Home Assistant
* monitoring
* development services 
* local AI

## Target hardware
- amd64 architecture (8 GB RAM, 512 GB SSD, Wi-Fi networking )
- Zigbee USB coordinator (example: Sonoff ZBDongle-P)  
  Keep the Zigbee coordinator on a USB extension cable 

## Design principles
1. Ubuntu Server is the host OS; Docker Compose runs application services.
2. Host-critical services (networking, SSH, Tailscale, firewall, Restic scheduling) remain on Ubuntu.
3. Each application group has an independent Compose project.
4. Deployment and updates are manual. Nothing in this repository automatically deploys from GitHub.
5. Persistent application data lives under `/srv/homelab/data`, outside the Git checkout.

## Documentation
- [Architecture](docs/architecture.md)
- [Installation](docs/installation.md)  
  ⚠️ read before executing anything
- [Networking](docs/networking.md)
- [Services](docs/services.md)
- [Backup and recovery](docs/backup-and-recovery.md)
- [Operations runbook](docs/operations.md)

## Installation

```bash
# Start selected projects.
./scripts/management/homelab.sh up smart-home
./scripts/management/homelab.sh status
```
Do not run every project at once on an 8 GB machine. Start with `smart-home`, `storage`, and `monitoring`. Start `development` and `ai` only when needed.

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


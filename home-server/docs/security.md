# Security baseline

## Public repository

This repository is intended to be public. Commit only templates and generic scripts.

Never commit:

- `.env` files
- passwords, API keys, tokens or OAuth credentials
- Tailscale auth keys
- SSH private keys
- MQTT password files
- Home Assistant `secrets.yaml`
- Zigbee network keys or coordinator backups
- personal files, database dumps or Restic repositories
- private certificates

If a secret is accidentally committed, removing it in a later commit is insufficient. Rotate the secret and clean Git history if necessary.

## Docker

- Do not expose Docker's TCP API.
- Do not mount `/var/run/docker.sock` into application containers unless essential.
- Avoid `privileged: true`.
- Use read-only mounts where possible.
- Pin image versions after testing them.
- Back up data before updates.
- Understand that membership in the `docker` group is effectively root access.

## Host

- Use SSH keys and disable password SSH login only after confirming key-based login works.
- Keep security updates enabled.
- Use Tailscale for remote access.
- Keep a recovery path if Wi-Fi or Tailscale fails.
- Use a firewall, but account for Docker-published port behavior.
- Do not expose administration interfaces to the public Internet.

## MQTT

The Compose template binds MQTT to `127.0.0.1:1883` on the host and uses a password file. Zigbee2MQTT connects over its internal Compose network. Do not change the bind to `0.0.0.0` without authentication and firewall review.

## Backups

Encrypt Restic repositories. Keep the repository password outside the backup disk and outside Git. Keep at least one copy off-site.

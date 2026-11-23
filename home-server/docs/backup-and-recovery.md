# Backup and recovery

## Backup policy

Back up application data and configuration to a separate external disk.  
A backup stored on the internal 512 GB SSD does not protect against SSD failure.

**Suggested backup targets:**
- `/srv/homelab/data`
- selected `/etc` configuration files
- personal files under `/srv/homelab/files`

For databases, create consistent dumps before backing up raw data directories. For PostgreSQL:

```bash
docker exec postgres pg_dumpall -U "$POSTGRES_USER" \
  > /mnt/homelab-backup/postgres-all.sql
```

Run this only when the development project is deployed and load the database credentials safely.

## Initialize Restic

Mount an external disk at `/mnt/homelab-backup`, then:

```bash
sudo apt install restic
sudo install -d -m 0700 /root/.config/restic
sudo sh -c 'umask 077; printf "%s" "REPLACE_WITH_LONG_RANDOM_SECRET" > /root/.config/restic/password'
sudo restic -r /mnt/homelab-backup/restic init
```

Do not put the actual password in shell history. Prefer a secure password manager and a protected root-owned password file. The example above is a placeholder procedure; replace it securely before use.

Run a backup:

```bash
sudo RESTIC_REPOSITORY=/mnt/homelab-backup/restic \
  RESTIC_PASSWORD_FILE=/root/.config/restic/password \
  restic backup /srv/homelab/data /srv/homelab/files
```

Check snapshots:

```bash
sudo RESTIC_REPOSITORY=/mnt/homelab-backup/restic \
  RESTIC_PASSWORD_FILE=/root/.config/restic/password \
  restic snapshots
```

## Restore test

A backup is not proven until a restore has been tested. Restore into a temporary directory first:

```bash
sudo mkdir -p /tmp/homelab-restore-test
sudo RESTIC_REPOSITORY=/mnt/homelab-backup/restic \
  RESTIC_PASSWORD_FILE=/root/.config/restic/password \
  restic restore latest --target /tmp/homelab-restore-test
```

Inspect the restored files before replacing live data.

## Recovery outline

1. Reinstall the same Ubuntu LTS release.
2. Restore network access and SSH.
3. Install Docker using the repository script.
4. Clone this GitHub repository.
5. Restore `/srv/homelab/data` from Restic.
6. Restore private `.env` and secrets from a secure password manager/off-site copy.
7. Reconnect the Zigbee coordinator using its stable `/dev/serial/by-id` path.
8. Start `smart-home`, then `storage` and `monitoring`.
9. Verify devices, automations, MQTT, backups and alerts.

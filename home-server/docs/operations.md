# Operations runbook

## Status

```bash
./scripts/management/homelab.sh status
docker stats --no-stream
free -h
df -h
```

## Logs

```bash
./scripts/management/homelab.sh logs smart-home
docker logs -f zigbee2mqtt
```

## Update one project manually

1. Read release notes for the service.
2. Back up persistent data.
3. Pull repository changes.
4. Review changed Compose files.
5. Pull images.
6. Validate Compose configuration.
7. Recreate the project.
8. Verify logs and application health.

```bash
git pull --ff-only
./scripts/management/homelab.sh pull smart-home
./scripts/management/homelab.sh config smart-home
./scripts/management/homelab.sh up smart-home
./scripts/management/homelab.sh status
```

## Resource pressure

```bash
free -h
docker stats --no-stream
ps aux --sort=-%mem | head
```

Stop optional workloads first:

```bash
./scripts/management/homelab.sh down ai
./scripts/management/homelab.sh down development
```

## Zigbee troubleshooting

```bash
ls -l /dev/serial/by-id/
docker logs --tail=200 zigbee2mqtt
docker exec zigbee2mqtt ls -l /dev/ttyUSB0
```

Do not delete Zigbee2MQTT data or re-pair devices as a first troubleshooting step. Back up the coordinator and application data before changing firmware or network settings.

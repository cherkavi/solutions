# Services and operating notes

## smart-home

- Home Assistant Container: host network for discovery; no Supervisor/add-ons.
- Mosquitto: MQTT broker, password authentication, host loopback publish.
- Zigbee2MQTT: USB coordinator passthrough, frontend on 8081.
- Persistent data: `/srv/homelab/data/{homeassistant,mosquitto,zigbee2mqtt}`.

## storage

- Syncthing synchronizes selected folders between trusted devices.
- GUI is bound to host loopback; use SSH port forwarding or adjust access deliberately.
- Synchronization is not backup: deletions and corruption can synchronize too.

## monitoring

- Uptime Kuma monitors endpoints and services.
- Add checks for Home Assistant, Zigbee2MQTT, MQTT TCP port, Internet reachability and disk space.
- This starter project avoids a full Prometheus/Grafana stack to conserve RAM.

## infrastructure

- Optional AdGuard Home.
- Do not make it the only DNS server until tested and a fallback is configured.
- DNS port 53 conflicts with other local DNS services and must be planned.

## development

- Gitea, PostgreSQL and Qdrant are on-demand.
- PostgreSQL and Qdrant are bound to host loopback in the starter configuration.
- Avoid running this project concurrently with Ollama on 8 GB RAM.

## ai

- Ollama is on-demand and bound to host loopback.
- Start with a small quantized model (roughly 1B–3B parameters).
- CPU inference may be slow; actual performance depends on CPU generation and memory.
- Keep context size modest. Model weights are not the only memory consumer.

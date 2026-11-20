# Smart home

Home Assistant Container, Mosquitto and Zigbee2MQTT.

Before startup:
1. Set `ZIGBEE_DEVICE` in the root `.env`.
2. Create `/srv/homelab/data/mosquitto/config/passwords` using `mosquitto_passwd`.
3. Copy and edit the Zigbee2MQTT configuration example into `/srv/homelab/data/zigbee2mqtt/configuration.yaml`.
4. Preserve existing Zigbee network data and coordinator backup when migrating.

Home Assistant uses host networking. Configure its MQTT integration to use `127.0.0.1:1883`. Zigbee2MQTT uses `mqtt://mosquitto:1883` on the Compose network.

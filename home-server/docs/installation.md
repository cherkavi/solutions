# Installation guide
## 0. prerequisites 
* you have main computer with installed Visual Code on it
* you have cloned this repo and using current file as a starting point
* your Ubuntu server is going to be installed on another computer

## 1. Install Ubuntu Server

### During installation:
- Select Ubuntu Server, not Desktop.
- Enable OpenSSH Server.
- Use a strong named administrator account.
- Optional: Prefer full-disk encryption if you can manage unattended reboot/unlock requirements.

### After first boot:
```bash
sudo apt update
sudo apt full-upgrade -y

## install your usual packages
#  "current-project/## headless/server

sudo reboot
```

### WiFi router settings 
Create a DHCP reservation for the server in your router (WiFi mesh).  

### check your SSH connection 
```sh
## create alias for connection: server-home-ssh
sshpass -p "$SERVER_PASSWORD" ssh "$SERVER_USER@$SERVER_HOST"

# example of the function 
function server-home-ssh(){
    SERVER_USER=$(keepass...)
    SERVER_PASSWORD=$(keepass... )
    SERVER_HOST=$(keepass... )
    # ssh-copy-id $SERVER_USER@$SERVER_HOST   # ssh $SERVER_USER@$SERVER_HOST

    if [ "$#" -gt 0 ]; then
        sshpass -p "$SERVER_PASSWORD" ssh "$SERVER_USER@$SERVER_HOST" "$*"
    else
        sshpass -p "$SERVER_PASSWORD" ssh "$SERVER_USER@$SERVER_HOST"
    fi    
}
function server-home-ssh-copy-to() {
    if [ "$#" -lt 2 ]; then
        echo "Usage: server-home-ssh-copy-to <src> <dest>" >&2
        return 1
    fi

    local SERVER_USER SERVER_PASSWORD SERVER_HOST SRC DEST
    SERVER_USER=$(keepass...)
    SERVER_PASSWORD=$(keepass... )
    SERVER_HOST=$(keepass... )
    SRC="$1"
    DEST="$2"

    sshpass -p "$SERVER_PASSWORD" scp -r "$SRC" "$SERVER_USER@$SERVER_HOST:$DEST"
}
```

### update remote bashrc
```sh
SERVER_USER=$(keepass...)
SERVER_PASSWORD=$(keepass... )
SERVER_HOST=$(keepass... )
cat ./scripts/lib/common.sh
cat ./scripts/lib/common.sh | sshpass -p "$SERVER_PASSWORD" ssh "$SERVER_USER@$SERVER_HOST" 'cat >> ~/.bashrc'

server-home-ssh
```

### [check your system after the installation](#check-your-system)

### Set hostname and timezone:
```bash
server-home-ssh

## hostname 
sudo hostnamectl 
# adjust it
sudo hostnamectl set-hostname home-server

## timezone 
sudo timedatectl
# adjust it 
sudo timedatectl set-timezone Europe/Berlin

exit
```

## 2. Adjust common variables in .env file 
### create .env file 
```bash
cp .env.example .env
cat .env
```

### Set `ZIGBEE_DEVICE` to the actual persistent device path
```sh
ZIGBEE_DEVICE=$(server-home-ssh ls /dev/serial/by-id/); echo $ZIGBEE_DEVICE
sed -i "s|^ZIGBEE_DEVICE=.*|ZIGBEE_DEVICE=/dev/serial/by-id/${ZIGBEE_DEVICE}|" .env
cat .env
```

### set default user
```sh
# PUID=1000  ## uid=
# PGID=1000  ## gid=
server-home-ssh id
```

## 3. Install host packages
Review scripts before running:
```bash
server-home-ssh

export DEBIAN_FRONTEND=noninteractive
log "Updating apt package index..."
sudo apt-get update

###############################
## Installing baseline packages
sudo apt-get install -y ca-certificates curl git jq vim htop tmux smartmontools nvme-cli lm-sensors restic ufw unattended-upgrades needrestart usbutils pciutils 
log "Enabling unattended security upgrades..."
sudo systemctl enable --now unattended-upgrades || true

#################
## install docker 
# alternative installation in scripts/02-install-docker.sh
sudo apt-get install -y docker.io docker-buildx docker-compose-v2

sudo groupadd docker
sudo usermod -aG docker $USER 

################################################
## create folders/persistent for upcoming docker containers 
BASE=/srv/homelab
sudo mkdir -p $BASE
sudo chown -R "$USER" "$BASE"
install -d -m 0755 "$BASE"/{data,files,backups,logs}
for d in homeassistant zigbee2mqtt mosquitto syncthing uptime-kuma adguard gitea postgresql qdrant ollama; do
  install -d -m 0750 "$BASE/data/$d"
done
install -d -m 0750 "$BASE/data/mosquitto"/{config,data,log}
install -d -m 0750 "$BASE/data/adguard"/{work,conf}
chmod 0700 "$BASE/backups"

sudo reboot
```
check installation 
```sh
server-home-ssh

sudo docker run --rm hello-world
docker compose version
```

## Prepare configurations 
### Configure Mosquitto
#### mosquitto passwords
```bash
###########
# file with passwords, if you are using it 
# create locally file with passwords with all the users: /tmp/mosquitto-passwords
mosquitto_passwd -b /tmp/mosquitto-passwords my_secret_user "my_secret_password"
server-home-ssh-copy-to /tmp/mosquitto-passwords /srv/homelab/data/mosquitto/config/passwords
```
or via docker
```sh
server-home-ssh
docker run --rm -it --user 0:0 -v /srv/homelab/data/mosquitto/config:/mosquitto/config eclipse-mosquitto:2 mosquitto_passwd -c /mosquitto/config/passwords zigbee
sudo chown 1883:1883 /srv/homelab/data/mosquitto/config/passwords
sudo chmod 0600 /srv/homelab/data/mosquitto/config/passwords
exit
```
#### mosquitto configs
```sh
cat config/mosquitto/mosquitto.conf.example2
server-home-ssh-copy-to config/mosquitto/mosquitto.conf.example2 /srv/homelab/data/mosquitto/config/mosquitto.conf

server-home-ssh
# The official Mosquitto container runs as UID 1883.
sudo chown -R 1883:1883 /srv/homelab/data/mosquitto
exit 
```

#### start docker compose 


Use a strong password. Configure the same username/password in Zigbee2MQTT's private `configuration.yaml`. Home Assistant can connect to `127.0.0.1:1883` because it uses host networking.

## 4. Configure Zigbee2MQTT
### start with init installation 
```bash
cat config/zigbee2mqtt/configuration.yaml.example
sudo cp config/zigbee2mqtt/configuration.yaml.example /srv/homelab/data/zigbee2mqtt/configuration.yaml
sudo chown -R "$USER":"$USER" /srv/homelab/data/zigbee2mqtt
nano /srv/homelab/data/zigbee2mqtt/configuration.yaml
```
Ensure the `serial.port` inside the container is `/dev/ttyUSB0`. The Compose file maps the host's `/dev/serial/by-id/...` path to that container path. Confirm the correct adapter type for your coordinator firmware.
For a Sonoff ZBDongle-P with Z-Stack firmware, `adapter: zstack` is commonly used. Do not change coordinator firmware or network settings during a simple server migration.

### copy your existing data files 
```
./docker-compose.yml
/srv/homelab/data/zigbee2mqtt/database.db
/srv/homelab/data/zigbee2mqtt/state.json
/srv/homelab/data/zigbee2mqtt/configuration.yaml
/srv/homelab/data/zigbee2mqtt/coordinator_backup.json
```




## 9. Start smart home

```bash
cd /opt/homelab-ubuntu
./scripts/management/homelab.sh config smart-home
./scripts/management/homelab.sh up smart-home
./scripts/management/homelab.sh status
```

Open Home Assistant at `http://SERVER_LAN_IP:8123` and Zigbee2MQTT at `http://SERVER_LAN_IP:8081`.

## 10. Deploy other projects gradually

```bash
./scripts/management/homelab.sh up storage
./scripts/management/homelab.sh up monitoring
```

Only when needed:

```bash
./scripts/management/homelab.sh up development
./scripts/management/homelab.sh up ai
```

Review resource use:

```bash
free -h
docker stats --no-stream
df -h
```

## 11. Manual update procedure

```bash
cd /opt/homelab-ubuntu
git pull --ff-only
./scripts/management/homelab.sh pull smart-home
./scripts/management/homelab.sh config smart-home
```

Back up persistent data before applying updates. Then explicitly recreate:

```bash
./scripts/management/homelab.sh up smart-home
```

The repository intentionally does not contain an auto-update container or GitHub Actions deployment workflow.


# Other steps
## check your system 
```sh
systemctl list-units --type=service --state=running
systemctl list-timers --all
sudo journalctl -f
```
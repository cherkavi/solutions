# Installation guide

## prerequisites 

* you have main computer with installed Visual Code on it
* you have cloned this repo and using current file as a starting point
* your Ubuntu server is going to be installed on another computer

## Install Ubuntu Server

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

## Adjust common variables in .env file 
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

## Install host packages
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
```

### check ports
```sh
# check all open listening ports 
sudo ss -tulnp
```

## Create folders
```sh
################################################
## create folders/persistent for upcoming docker containers 
BASE=/srv/homelab
sudo mkdir -p $BASE
sudo chown -R "$USER" "$BASE"
install -d -m 0755 "$BASE"/{data,files,backups,logs,docker}
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

## Smart Home Configuration 

### Mosquitto check installation 
```sh
## installation via package manager
# sudo apt install -y mosquitto 
mosquitto

## installation during Ubuntu installation 
# snap install mosquitto
snap list | grep mosquitto
sudo snap remove mosquitto
```

#### mosquitto config
```sh
server-home-ssh cat /etc/mosquitto/mosquitto.conf
```
configuration example
```
persistence true
persistence_location /mosquitto/data/
log_dest stdout

listener 1883 0.0.0.0
allow_anonymous false
password_file /mosquitto/config/passwords
```

#### mosquitto passwords
```sh
mosquitto_passwd -b /tmp/mosquitto-passwords my_secret_user "my_secret_password"
```

#### start mosquitto
```sh
sudo systemctl enable --now mosquitto
sudo systemctl status mosquitto
```

### Configure Mosquitto in docker 
#### mosquitto passwords
Configure the same username/password in Zigbee2MQTT's private `configuration.yaml`. 
Home Assistant can connect to `127.0.0.1:1883` because it uses host networking.
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

### Configure Zigbee2MQTT
#### start with init installation 
```bash
cat config/zigbee2mqtt/configuration.yaml.example2
server-home-ssh-copy-to config/zigbee2mqtt/configuration.yaml.example2 /srv/homelab/data/zigbee2mqtt/configuration.yaml

server-home-ssh
sudo chown -R "$USER":"$USER" /srv/homelab/data/zigbee2mqtt
exit
```
Ensure the `serial.port` inside the container is `/dev/ttyUSB0`. The Compose file maps the host's `/dev/serial/by-id/...` path to that container path. Confirm the correct adapter type for your coordinator firmware.
For a Sonoff ZBDongle-P with Z-Stack firmware, `adapter: zstack` is commonly used. Do not change coordinator firmware or network settings during a simple server migration.


#### copy your existing data files 
```sh
SOURCE_FOLDER_ZIGBEE=/opt/zigbee2mqtt/data

server-home-ssh-copy-to $SOURCE_FOLDER_ZIGBEE/database.db /srv/homelab/data/zigbee2mqtt/database.db
server-home-ssh-copy-to $SOURCE_FOLDER_ZIGBEE/state.json /srv/homelab/data/zigbee2mqtt/state.json
server-home-ssh-copy-to $SOURCE_FOLDER_ZIGBEE/configuration.yaml /srv/homelab/data/zigbee2mqtt/configuration.yaml
server-home-ssh-copy-to $SOURCE_FOLDER_ZIGBEE/coordinator_backup.json /srv/homelab/data/zigbee2mqtt/coordinator_backup.json

server-home-ssh
sudo chown -R "$USER":"$USER" /srv/homelab/data/zigbee2mqtt
exit
```

### copy compose configuration
```sh
server-home-ssh-copy-to compose/smart-home/compose.yaml /srv/homelab/docker/zigbee2mqtt/compose.yaml 
cat .env
server-home-ssh-copy-to .env /srv/homelab/docker/zigbee2mqtt/.env 
```


## Smart Home start
```bash
server-home-ssh 

docker ps
## check config 
docker compose -f /srv/homelab/docker/zigbee2mqtt/compose.yaml config

## start containers
# docker compose -f /srv/homelab/docker/zigbee2mqtt/compose.yaml up -d --force-recreate
docker compose -f /srv/homelab/docker/zigbee2mqtt/compose.yaml up -d
# docker compose -f /srv/homelab/docker/zigbee2mqtt/compose.yaml down

## logs 
docker compose -f /srv/homelab/docker/zigbee2mqtt/compose.yaml logs -f mosquitto zigbee2mqtt homeassistant
```

```sh
x-www-browser http://SERVER_LAN_IP:8123
x-www-browser http://SERVER_LAN_IP:8081
```


## TODO: Deploy other projects gradually
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

## TODO: Manual update procedure

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


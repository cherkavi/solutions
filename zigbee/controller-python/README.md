# Python application for Zigbee devices

## installation 
```sh
python3 -m venv .venv

source .venv/bin/activate

pip install paho-mqtt
```


## execute monitor
```sh
python monitor.py --help
python monitor.py run
python monitor.py status
python monitor.py history --sensor three --limit 100
```

## service
### create service 
```sh
sudo tee /etc/systemd/system/zigbee-monitor.service <<EOF
[Unit]
Description=Zigbee Sensor Monitor
After=network.target mosquitto.service
Requires=mosquitto.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/zigbee-monitor
ExecStart=$HOME/zigbee-monitor/.venv/bin/python $HOME/zigbee-monitor/monitor.py run
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```
### enable service
```sh
## start daemon 
sudo systemctl daemon-reload
sudo systemctl enable --now zigbee-monitor

## status 
sudo systemctl status zigbee-monitor
sudo systemctl restart zigbee-monitor

## log
journalctl -u zigbee-monitor -f
```
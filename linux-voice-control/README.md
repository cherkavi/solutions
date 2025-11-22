# voice commands for Ubuntu computer

## SetUp bluetooth device ( any keypad ) to read data from it 

### list of all connected bluetooth devices 
```sh   
bluetoothctl devices Connected
# Device 3F:3A:C2:DF:F0:81 J06
```

### detect pressed button by code 
```sh
sudo evtest  # detect pressed button 

# Event: time 1763798603.717814, -------------- SYN_REPORT ------------
# Event: time 1763798615.668735, type 1 (EV_KEY), code 201 (KEY_PAUSECD), value 1
# Event: time 1763798615.668735, -------------- SYN_REPORT ------------
# Event: time 1763798615.733838, type 1 (EV_KEY), code 201 (KEY_PAUSECD), value 0
# Event: time 1763798615.733838, -------------- SYN_REPORT ------------
```

### service for listening pressed button and react on them
```sh
# installation 
sudo apt install triggerhappy

# setup 
sudo vim /etc/triggerhappy/triggers.d/headset.conf  
# # <Event Name>  <Value>  <Command>  # 4 space delimiter
# ABS_Y     0        /home/soft/key-reaction-headset.sh
# KEY_VOLUMEDOWN    0    /home/soft/key-reaction-headset.sh

# prepare dummy logic
echo "date >> /home/soft/triggerhappy.log" > /home/soft/key-reaction-headset.sh

# prepare log files 
touch /home/soft/triggerhappy.log
chmod 666 /home/soft/triggerhappy.log

# service start
sudo systemctl restart triggerhappy
sudo systemctl status triggerhappy  # status and last log output

## service log
sudo journalctl -u triggerhappy -f
sudo journalctl -u triggerhappy -b --no-pager
```

## Record voice
> record voice from microphone during 3 sec and save to mp3
### installation
```sh
sudo apt install ffmpeg
sudo apt install audacity # for editing sounds https://mixkit.co/free-sound-effects/
```

```sh
# play beep 
ffplay -nodisp -autoexit /home/soft/beep.mp3

# record audio 
rm /home/soft/command.mp3; ffmpeg -f pulse -i default -t 3 /home/soft/command.mp3

# play beep 
ffplay -nodisp -autoexit /home/soft/beep.mp3

```

## Decode voice and run the logic 
### installation
```sh
x-www-browser https://github.com/cherkavi/python-utilities/tree/master/voice
```

### voice recognition
```sh
# decode text 
source /home/projects/github-mirror/python-utilities/voice/virtual-env/bin/activate
python /home/projects/github-mirror/python-utilities/voice/mp3-transcript.py /home/soft/command.mp3
```
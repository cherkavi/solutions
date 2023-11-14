# Razer Tartarus Razer Nostromo buttons mapping
current project will help to use Razer Tartarus and Razer Nostromo   
for your left hand when you are drawing on your Wacom tablet with right hand   
in next applications:
* [excalidraw](https://excalidraw.com)
* [VisualParadigm](https://online.visual-paradigm.com/)
* [sketchtogether](https://app.sketchtogether.com/)
  * execute also ``` sudo python3 sketch-automation.py``` and play with ALT+buttons
* ksnip

## select your device
```sh
sudo evtest
# select your Keypad device
# 
# Input device ID: bus 0x3 vendor 0x1532 product 0x22b version 0x111
# 1. convert it to:   b0003   v1532         p022B          e0111
# 2. convert it to: evdev:input:b0003v1532p022Be0111*
```

## create file with mapping 
```sh
# create mapping file for HWDB
sudo touch /etc/udev/hwdb.d/90-keypad-custom.hwdb
sudo chmod 777 /etc/udev/hwdb.d/90-keypad-custom.hwdb
```

[keys name, key mapping names](https://hal.freedesktop.org/quirk/quirk-keymap-list.txt)
> example for sketchtogether & ksnip 
```hwdb
evdev:input:b0003v1532p022Be0111*
# keys: 01-05
 KEYBOARD_KEY_7001e=b
 KEYBOARD_KEY_7001f=a
 KEYBOARD_KEY_70020=l
 KEYBOARD_KEY_70021=r
 KEYBOARD_KEY_70022=t
# keys: 06-10
 KEYBOARD_KEY_7002b=q
 KEYBOARD_KEY_70014=w
 KEYBOARD_KEY_7001a=g
 KEYBOARD_KEY_70008=h
 KEYBOARD_KEY_70015=c
# keys: 11-15
 KEYBOARD_KEY_70039=1
 KEYBOARD_KEY_70004=2
 KEYBOARD_KEY_70016=3
 KEYBOARD_KEY_70007=4
 KEYBOARD_KEY_70009=5
# keys: 16-19
 KEYBOARD_KEY_700e1=leftctrl
 KEYBOARD_KEY_7001d=z
 KEYBOARD_KEY_7001b=v
 KEYBOARD_KEY_70006=6
# cursor FDBU
 KEYBOARD_KEY_70052=1
 KEYBOARD_KEY_7004f=5
 KEYBOARD_KEY_70051=2
 KEYBOARD_KEY_70050=3
# cursor buttons 
 KEYBOARD_KEY_700e2=leftalt
 KEYBOARD_KEY_7002c=leftshift
```

> nostromo sketchtogether mapping  
Input device ID: bus 0x3 vendor 0x1532 product 0x111 version 0x111
```hwdb
evdev:input:b0003v1532p0111e0111*
 KEYBOARD_KEY_70039=1
 KEYBOARD_KEY_70004=2
 KEYBOARD_KEY_70016=3
 KEYBOARD_KEY_70007=4
 KEYBOARD_KEY_70009=5
 KEYBOARD_KEY_70006=6
 KEYBOARD_KEY_70015=t
 KEYBOARD_KEY_70008=c
 KEYBOARD_KEY_70052=right
 KEYBOARD_KEY_70051=left
 KEYBOARD_KEY_70050=up
 KEYBOARD_KEY_7004f=down
 KEYBOARD_KEY_7002c=leftshift
 KEYBOARD_KEY_700e2=leftalt
 KEYBOARD_KEY_700e1=leftctrl
 KEYBOARD_KEY_7001b=v
 KEYBOARD_KEY_7001d=z
 KEYBOARD_KEY_7002b=delete
```


```sh
# apply mapping 
sudo udevadm hwdb --update
sudo udevadm trigger

# or 
sudo systemd-hwdb update
sudo udevadm trigger --sysname-match="event*"
```

```bash
# troubleshooting
ls /dev/input/by-id/*-kbd
# check yours url: evdev:input:b0003v1532p022be0111*
sudo udevadm --debug test `udevadm info -q path -n /dev/input/by-id/usb-Razer_Razer_Tartarus_V2-if01-event-kbd`
sudo udevadm --debug test `udevadm info -q path -n /dev/input/by-id/usb-Razer_Razer_Tartarus_V2-event-kbd`
# need to be changed to: evdev:input:b0003v1532p022Be0111*
```


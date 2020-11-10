```sh
sudo evtest
# event21
# Input device ID: bus 0x3 vendor 0x1532 product 0x22b version 0x111
```

```sh
# create mapping file for HWDB
sudo rm /etc/udev/hwdb.d/90-razer-keypad.hwdb
sudo vim /etc/udev/hwdb.d/90-razer-keypad.hwdb
```
[mapping names](https://hal.freedesktop.org/quirk/quirk-keymap-list.txt)
> made for sketchtogether & ksnip 
```text
evdev:input:b0003v1532p022Be0111*
 KEYBOARD_KEY_70039=1
 KEYBOARD_KEY_70004=2
 KEYBOARD_KEY_70016=3
 KEYBOARD_KEY_70007=4
 KEYBOARD_KEY_70009=5
 KEYBOARD_KEY_70006=6
 KEYBOARD_KEY_70052=right
 KEYBOARD_KEY_70051=left
 KEYBOARD_KEY_70050=up
 KEYBOARD_KEY_7004f=down
 KEYBOARD_KEY_7002c=leftshift
 KEYBOARD_KEY_700e2=leftalt
 KEYBOARD_KEY_700e1=leftctrl
 KEYBOARD_KEY_7001b=v
 KEYBOARD_KEY_7001d=z
 KEYBOARD_KEY_7001e=p
 KEYBOARD_KEY_7001f=a
 KEYBOARD_KEY_70020=l
 KEYBOARD_KEY_70021=r
 KEYBOARD_KEY_70022=e
 KEYBOARD_KEY_70015=n
```

nostromo sketchtogether mapping
Input device ID: bus 0x3 vendor 0x1532 product 0x111 version 0x111
```
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

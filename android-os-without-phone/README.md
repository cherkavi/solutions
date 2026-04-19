# Start android on PC

## Waydroid
### [waydroid installation](https://docs.waydro.id/usage/install-on-desktops)
```sh
## download certificate 
curl https://repo.waydro.id/waydroid.gpg > temp.gpg # vim temp.gpg
sudo mv temp.gpg /usr/share/keyrings/waydroid.gpg

## update repository with new list
export DISTRO=$(lsb_release -c | grep Codename | awk '{print $2}'); echo $DISTRO
echo "deb [signed-by=/usr/share/keyrings/waydroid.gpg] https://repo.waydro.id/ $DISTRO main" > temp.list # cat temp.list
sudo mv temp.list /etc/apt/sources.list.d/waydroid.list   

## install waydroid
sudo apt update && sudo apt install waydroid
```
### waydroid image install 
* [manual download ](https://sourceforge.net/projects/waydroid/)
* [download example](https://sourceforge.net/projects/waydroid/files/images/vendor/waydroid_x86_64/lineage-20.0-20260403-MAINLINE-waydroid_x86_64-vendor.zip/download)
```sh
waydroid status

sudo waydroid init --help

## To install with Google Play Store
sudo waydroid init -s GAPPS

## install custom image 
sudo waydroid init -s GAPPS -i https://example.com/path/to/custom_image.zip
```

### waydroid image start 
```sh
## set multiwindow mode
waydroid prop set persist.waydroid.multi_windows true 
## container start 
sudo waydroid container start

waydroid status


## new terminal session - start the session 
waydroid session start  
waydroid session stop

## new UI session
waydroid show-full-ui

## start container after `init`
sudo systemctl start waydroid-container
```

## [Genymotion](https://www.genymotion.com/product-desktop/download/)
for emulating specific hardware
```sh
curl https://dl.genymotion.com/releases/genymotion-3.10.0/genymotion-3.10.0-linux_x64.run
chmod +x ~/Downloads/genymotion-3.10.0-linux_x64.run
cd /home/soft
~/Downloads/genymotion-3.10.0-linux_x64.run
rm ~/Downloads/genymotion-3.10.0-linux_x64.run

genymotion
```

## Android OS for PC
* **[FydeOS](https://fydeos.io/download)**
  > chromium fork
* [Windows Subsystem](https://quickfever.com/how-to-install-android-apps-on-windows-11-from-apk-file/)

## VirtualBox
* **[Android-x86](https://www.osboxes.org/android-x86)**
  * [original source, iso](https://www.android-x86.org/)
  * [github](https://android-x86.github.io/)
* [Lineage OS](https://www.osboxes.org/android-x86/)
  * create new Virtual Machine
  * Type: Linux, Version: Linux 2.6/3.x/4.x (64-bit)
  * Memory: 4Gb
  * Use an existing virtual hard disk file ( <--- select your vdi )
* Phoenix OS

## ISO images
* [lineage os](https://www.android-x86.org/releases/releasenote-cm-x86-14-1-r5.html)
* [android os](https://www.android-x86.org/)
How to run it:
1. Install Android
2. Restart
3. Start 'Android LIVE'
4. Android menu: Autoinstall to HardDisk

## Emulator
* Android Studio
* Phoenix OS
* [BlueStacks](https://www.bluestacks.com/de/index.html) - only Win,Mac
* NoxPlayer
* MEmu Play.

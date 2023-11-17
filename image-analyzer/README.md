# Image analyzer

## Description
There are many images and videos on the diff discs.
Main goal of current application:
1. to have one "Master" SDD disc with all images
2. to have one "Copy of master" HDD disc with all images

## Steps:
### 1. create file "files-all-${DISK_NAME}.psv"
```sh
# <md5sum> | <file name> | <file path>
DISK_NAME="archive2"
PATH_TO_DISK=/media/$USER/$DISK_NAME
./md5-sum-collector.sh  $PATH_TO_DISK > files-all-${DISK_NAME}.psv
```
### 2. sort records:
```sh
FILES_ON_DISK=files-all-${DISK_NAME}.psv
FILES_SORTED_BY_MD5=files-sort-md5-${DISK_NAME}.psv
cat $FILES_ON_DISK | sort > $FILES_SORTED_BY_MD5
```
### 3. find duplicates in md5sum 
```sh
SORTED_MD5=md5-<disk name>.psv
cat $FILES_SORTED_BY_MD5 | awk -F '|' '{print $1}' > $SORTED_MD5
cat $SORTED_MD5 | uniq -d
```
### 4. collect files for all the disks
```sh
DISK_NAME="hdd1"
DISK_NAME="hdd2"
DISK_NAME="hdd3"
```

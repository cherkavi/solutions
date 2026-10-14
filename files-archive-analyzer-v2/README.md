# Archive disc #1

## init
```sh
DISC_NUM=1

PATH_MD5_FILENAME=~/photo-archive-${DISC_NUM}.tsv
PATH_MD5=~/photo-archive-${DISC_NUM}.tsv.md5sum

ls -la $PATH_MD5_FILENAME
ls -la $PATH_MD5
```

## collect md5sum 
```sh
cd photo
ls -la $PATH_MD5_FILENAME
# rm $PATH_MD5_FILENAME

./collect-md5sum.sh  $PATH_MD5_FILENAME
# waiting for "Done !"
```

## find all duplicated md5sum
```sh
head $PATH_MD5_FILENAME
wc -l ${PATH_MD5_FILENAME}
cat ${PATH_MD5_FILENAME} | awk -F '\t' '{print $1}' | sort | uniq -d > $PATH_MD5
wc -l $PATH_MD5

## print duplicates
for each_md5 in $(cat $PATH_MD5); do
    cat ${PATH_MD5_FILENAME} | grep $each_md5
done
```

## check if new folder with photo already saved in the previously collected one 
### collect files in the new folder 
```sh
PATH_TOCHECK_MD5_FILENAME=~/my-pictures-${DISC_NUM}.tsv
PATH_TOCHECK=~/Downloads/my-pictures
PATH_TOCOPY_MD5_FILENAME=~/my-pictures-${DISC_NUM}.tsv.tocopy

./collect-md5sum.sh  $PATH_TOCHECK_MD5_FILENAME $PATH_TOCHECK
wc -l $PATH_TOCHECK_MD5_FILENAME
head $PATH_TOCHECK_MD5_FILENAME
```

```sh
awk '
    NR == FNR {
        hashes[$1] = 1
        next
    }
    !($1 in hashes) {
        print
    }
' "$PATH_MD5_FILENAME" "$PATH_TOCHECK_MD5_FILENAME"  > $PATH_TOCOPY_MD5_FILENAME
wc -l $PATH_TOCHECK_MD5_FILENAME
wc -l $PATH_TOCOPY_MD5_FILENAME
```

### copy files 
```sh
find $DESTINATION_PATH | wc -l
DESTINATION_PATH=./2026-my

./copy-md5sum-files.sh $PATH_TOCHECK $DESTINATION_PATH $PATH_TOCOPY_MD5_FILENAME
## remove source
# [[ -n "$PATH_TOCHECK" && "$PATH_TOCHECK" != "/" && "$(realpath -m -- "$PATH_TOCHECK")" != "/" && "$(realpath -m -- "$PATH_TOCHECK")" != "$(pwd -P)" ]] && rm -rf -- "$PATH_TOCHECK"
find $DESTINATION_PATH | wc -l
find $PATH_TOCHECK | wc -l 
```
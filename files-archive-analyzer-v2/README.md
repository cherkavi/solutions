# Sync archives

## init
```sh
DISC_NUM=1
# DISC_NUM=2

PATH_MD5_FILENAME=~/photo-archive-${DISC_NUM}.tsv
PATH_MD5=~/photo-archive-${DISC_NUM}.tsv.md5sum

ls -la $PATH_MD5_FILENAME
ls -la $PATH_MD5
```

## collect md5sum 
```sh
DESTINATION_PATH_1="/media/$USER/Seagate Backup Plus Drive/photo"; cd $DESTINATION_PATH_1
DESTINATION_PATH_2="/media/$USER/archive2/photo"; cd $DESTINATION_PATH_2

ls -la $PATH_MD5_FILENAME
# rm $PATH_MD5_FILENAME

$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/collect-md5sum.sh  $PATH_MD5_FILENAME
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

## remove more later versions of the duplicates
```

## compare files from disk#1 and disk#2
```sh
# collect md5sum 
PATH_MD5_FILENAME_1=~/photo-archive-1.tsv
wc -l $PATH_MD5_FILENAME_1
head $PATH_MD5_FILENAME_1

PATH_MD5_FILENAME_2=~/photo-archive-2.tsv
wc -l $PATH_MD5_FILENAME_2
head $PATH_MD5_FILENAME_2

$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/uniqueness-calculator.sh  $PATH_MD5_FILENAME_1 $PATH_MD5_FILENAME_2
head $PATH_MD5_FILENAME_1-diff
head $PATH_MD5_FILENAME_2-diff
```

## copy missed files
```sh
DESTINATION_PATH_1="/media/$USER/Seagate Backup Plus Drive/photo"
DESTINATION_PATH_2="/media/$USER/archive2/photo"

cd $DESTINATION_PATH_1
$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/check-missed-files.sh  $PATH_MD5_FILENAME_1-diff
$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/copy-missed-files.sh  $PATH_MD5_FILENAME_1-diff "$DESTINATION_PATH_2"

cd $DESTINATION_PATH_2
$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/check-missed-files.sh  $PATH_MD5_FILENAME_2-diff
$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/copy-missed-files.sh  $PATH_MD5_FILENAME_2-diff "$DESTINATION_PATH_1"
```


## check if NEW folder with photo already saved in the previously collected one 
### collect md5sum for files in the NEW folder
```sh
PATH_TOCHECK_MD5_FILENAME=~/my-pictures-${DISC_NUM}.tsv
PATH_TOCHECK=~/Downloads/my-pictures
PATH_TOCOPY_MD5_FILENAME=~/my-pictures-${DISC_NUM}.tsv.tocopy

$HOME_PROJECTS_GITHUB/solutions/files-archive-analyzer-v2/collect-md5sum.sh  $PATH_TOCHECK_MD5_FILENAME $PATH_TOCHECK
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
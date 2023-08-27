1. copy from/via ftp
```sh
# go to temp folder
temp
# create temp folder 
mkdir anki; cd anki

# copy data from the remove machine/phone, from folder 'sketches'
ftp -P $NOTE8_FTP_PORT -inv $NOTE8_FTP_HOST  <<EOF
user vitalii vitalii
cd sketches
lcd .
mget *
quit
EOF

# remove all files from remote folder, when you need
ftp -P $NOTE8_FTP_PORT -inv $NOTE8_FTP_HOST  <<EOF
user vitalii vitalii
cd sketches
mdelete *
quit
EOF


2. add prefix to files  anki-wordcards
```sh
CUSTOM_PREFIX=anki-wordcards
add-prefix-to-all-files $CUSTOM_PREFIX
```

3. replace spaces in names of files
```sh
all-files-replace-space
```

4. Check all images for proper rotation position !
```sh 
nautilus .
```

5. for all files in current folder, upload to external image storage and save it on Dropbox
```sh
all-files-img-upload-archive
```

6. read last uploaded files and create anki mapping 
```sh
ANKI_IMPORT_FILE=$CUSTOM_PREFIX.anki-import.txt
# check files to be imported
COMMAND_RETRIEVE='cat $ARCHIVE_IMGBB_LIST | grep "${CUSTOM_PREFIX}2023-08-27-16" | sort -V '
```
create Anki Note like "Odd-Even"
```sh
# create header for anki-import file
echo '#separator:tab
#html:true
#tags column:3' > $ANKI_IMPORT_FILE
eval $COMMAND_RETRIEVE | awk -F ',' '{print $2}' | awk -f $HOME_PROJECTS_GITHUB/bash-example/awk/shrink-lines-to-columns.awk | awk -F '<=>' '{print $1" "$2}' | awk '{print "\"<img src=\"\""$1"\"\">\"\t""\"<img src=\"\""$2"\"\">\""}' >> $ANKI_IMPORT_FILE
```

7. import prepared file to anki
```sh
cat $ANKI_IMPORT_FILE
```


------------------
```sh
function add-prefix-to-all-files(){ 
    if [[ -z $1 ]]; then
        echo "pls, provide prefix for file";
    fi;
    new_prefix_name=$1;
    find . -type f -print0 | while IFS= read -r -d '' each_file; do
        prefix="./";
        file_name=${each_file#$prefix};
        echo $file_name "  >>> " $new_prefix_name$file_name;
        mv "$file_name" "$new_prefix_name$file_name";
    done
}

function all-files-replace-space(){ 
    find . -type f -print0 | while IFS= read -r -d '' each_file; do
        prefix="./";
        file_name=${each_file#$prefix};
        new_file_name=`echo $file_name | tr ' ' '_'`;
        mv "$file_name" "$new_file_name";
    done
}

```
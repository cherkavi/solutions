# Anki 
## fix manually collections in DB
```sh
# db place
$USER/.local/share/Anki2/{anki_account_email_address}

sqlite3 collection.anki2
```
```sql
select * from decks;
select * from cards;

SELECT id, flds FROM notes WHERE flds LIKE '%gewissen%'; -- id of record 
-- 	Field data, joined by \x1f (unit separator) — e.g., "Front text\x1fBack text"
UPDATE notes SET flds = 'updated\x1ftext', mod = strftime('%s','now') WHERE id = 1743965509382;
```

## save images to Anki for learning

### Alternatives
* https://quizlet.com/
* https://www.brainscape.com/

### Steps
1. copy images from/via ftp
```sh
# go to temp folder
temp
# create temp folder 
mkdir anki; cd anki

# copy data from the remote machine/phone via FTP ( user:vitalii, password: vitalii )
# from folder 'sketches'
ftp -P $NOTE8_FTP_PORT -inv $NOTE8_FTP_HOST  <<EOF
user vitalii vitalii
cd sketches
lcd .
mget *
quit
EOF

# Optional step 
# remove all files from remote folder via FTP ( user:vitalii, password: vitalii ) 
ftp -P $NOTE8_FTP_PORT -inv $NOTE8_FTP_HOST  <<EOF
user vitalii vitalii
cd sketches
mdelete *
quit
EOF


2. for creating uniqueness in cloud/dropbox/nas storage - add prefix to files  anki-wordcards
> check functions in https://github.com/cherkavi/bash-example.git
```sh
CUSTOM_PREFIX=card-word-
add-prefix-to-all-files $CUSTOM_PREFIX
```

3. replace space-char in filenames
```sh
all-files-replace-space
```

4. Check all images for proper rotation position !
```sh 
nautilus .
```

5. for all files in current folder, upload to external image storage ( save it on Dropbox )
```sh
all-files-img-upload-archive
# result of this operation will be: 
# 1. uploading to cloud storage
# 2. obtaining url to cloud storage ( publically accessible )
```

6. read last uploaded files and create anki mapping 
```sh
CUSTOM_PREFIX=card-word-
ANKI_IMPORT_FILE=$CUSTOM_PREFIX.anki-import.txt
# check files to be imported
cat $ARCHIVE_IMGBB_LIST | grep "${CUSTOM_PREFIX}" | sort -V | wc -l
# create command for using during import file creation
COMMAND_RETRIEVE='cat $ARCHIVE_IMGBB_LIST | grep "${CUSTOM_PREFIX}" | sort -V '
```
create Anki Note (import ready file) like "Odd-Even" ( front and back image for each card )
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

### shared scripts 
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
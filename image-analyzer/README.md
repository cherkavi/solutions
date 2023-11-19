# Image analyzer

## Description
There are many images and videos on the diff discs.
Main goal of current application:
1. to have one "Master" SDD disc with all images
2. to have one "Copy of master" HDD disc with all images

## Steps:
### 1. Collect files from all disks in psv file
> mostly human-involved operation
```sh
### 1. create file "files-all-${DISK_NAME}.psv"
# <md5sum> | <file name> | <file path>
DISK_NAME="archive2"
PATH_TO_DISK=/media/$USER/$DISK_NAME
ls $PATH_TO_DISK
OUTPUT_FILE=files-all-${DISK_NAME}.psv
./md5-sum-collector.sh  "$PATH_TO_DISK"  "$OUTPUT_FILE"
wc -l $OUTPUT_FILE
```

### 2. Analyze all *.psv files
* '-duplicated' - md5sum of duplications
* '-duplicated-folders' - folders with duplications
* '-report' - duplication report 
```sh
IFS=$'\n'
for OUTPUT_FILE in `ls *.psv`; do
    cat $OUTPUT_FILE | awk -F '|' '{print $1}' > ${OUTPUT_FILE}-md5
    cat ${OUTPUT_FILE}-md5 | sort > "$OUTPUT_FILE-sorted"
    rm "${OUTPUT_FILE}-md5"
    
    uniq -d "$OUTPUT_FILE-sorted" > "$OUTPUT_FILE-md5-duplicated"
    rm "$OUTPUT_FILE-sorted"

    OUTPUT_FILE_DUPLICATED_FOLDERS="$OUTPUT_FILE-duplicated-folders"
    printf "\n find duplicates in file: ${OUTPUT_FILE}"
    
    echo -n "" > $OUTPUT_FILE_DUPLICATED_FOLDERS
    for each_duplicated in `cat $OUTPUT_FILE-md5-duplicated`; do
        cat $OUTPUT_FILE | grep "^$each_duplicated" | awk -F '|' '{print $3}' | awk -F '/' '
            {
                for (i=1; i<=NF-1; i++) {
                    if (result != "" ){
                        result=result"/"$i    
                    } else {
                        result=$i
                    }
                } 
                print "/"result;
                result=""
            }
        ' >> $OUTPUT_FILE_DUPLICATED_FOLDERS
        cat $OUTPUT_FILE_DUPLICATED_FOLDERS | sort | uniq > ${OUTPUT_FILE_DUPLICATED_FOLDERS}-temp
        mv ${OUTPUT_FILE_DUPLICATED_FOLDERS}-temp $OUTPUT_FILE_DUPLICATED_FOLDERS
    done 

    OUTPUT_FILE_DUPLICATED="$OUTPUT_FILE-duplicated"
    echo -n "" > $OUTPUT_FILE_DUPLICATED
    for each_duplicated in `cat $OUTPUT_FILE-md5-duplicated`; do
        cat $OUTPUT_FILE | grep "^$each_duplicated" | awk -F '|' '{sub(/\/[^\/]*$/, ""); print $3"|"$2"|"$1}'  >> $OUTPUT_FILE_DUPLICATED
    done
    rm $OUTPUT_FILE-md5-duplicated
    
    cat $OUTPUT_FILE_DUPLICATED | sort > $OUTPUT_FILE_DUPLICATED-sorted
    mv $OUTPUT_FILE_DUPLICATED-sorted $OUTPUT_FILE_DUPLICATED
    
    OUTPUT_FILE_REPORT="$OUTPUT_FILE-report"
    echo -n "" > $OUTPUT_FILE_REPORT
    for each_duplicated_folder in `cat $OUTPUT_FILE_DUPLICATED_FOLDERS`; do
        echo $each_duplicated_folder >> $OUTPUT_FILE_REPORT
        for each_duplicate_file in `cat $OUTPUT_FILE_DUPLICATED | grep "^$each_duplicated_folder|"`; do
            echo "$each_duplicate_file" >> $OUTPUT_FILE_REPORT
            duplication_file_md5sum=`echo $each_duplicate_file | awk -F '|' '{print $3}'`
            for each_repeated_duplication_file in `cat $OUTPUT_FILE_DUPLICATED | grep "${duplication_file_md5sum}\$"`; do
                if [[ $each_repeated_duplication_file != $each_duplicate_file ]]; then
                    echo "  $each_repeated_duplication_file" >> $OUTPUT_FILE_REPORT
                fi
            done
        done 
    done
done

wc -l *psv*
```

### 2. compare two disks
* '-uniq' files contain information about uniq files on the disk
```sh
FILE_1=files-all-archive-2.psv
FILE_2=files-all-archive-original.psv

cat $FILE_1 | awk -F '|' '{print $1}' | sort > ${FILE_1}-md5-sort
cat $FILE_2 | awk -F '|' '{print $1}' | sort > ${FILE_2}-md5-sort

# list of uniq files in FILE_1
FILE_1_UNIQ=${FILE_1}-uniq
echo -n > ${FILE_1_UNIQ}
for each_md5_compare_line in `diff ${FILE_1}-md5-sort ${FILE_2}-md5-sort | grep '<'`; do
    each_md5=`echo $each_md5_compare_line | awk '{print $2}'`
    cat ${FILE_1} | grep "${each_md5}" | awk -F '|' '{print $3}' >> ${FILE_1_UNIQ}
done
cat ${FILE_1_UNIQ} | sort > "${FILE_1_UNIQ}-sorted"
mv "${FILE_1_UNIQ}-sorted" ${FILE_1_UNIQ}


# list of uniq files in FILE_2
FILE_2_UNIQ=${FILE_2}-uniq
echo -n > ${FILE_2_UNIQ}
for each_md5_compare_line in `diff ${FILE_1}-md5-sort ${FILE_2}-md5-sort | grep '>'`; do
    each_md5=`echo $each_md5_compare_line | awk '{print $2}'`
    cat ${FILE_2} | grep "${each_md5}" | awk -F '|' '{print $3}' >> ${FILE_2_UNIQ}
done
cat ${FILE_2_UNIQ} | sort > "${FILE_2_UNIQ}-sorted"
mv "${FILE_2_UNIQ}-sorted" ${FILE_2_UNIQ}
```

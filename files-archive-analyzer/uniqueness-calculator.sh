if [[ -z $1 ]]; then
    echo "no first file for analyzing"
    exit 1
fi
if [[ -z $2 ]]; then 
    echo "no second file specified"
    exit 2
fi

FILE_1=$1
FILE_2=$2

cat $FILE_1 | awk -F '|' '{print $1}' | sort > ${FILE_1}-md5-sort
cat $FILE_2 | awk -F '|' '{print $1}' | sort > ${FILE_2}-md5-sort

# list of uniq files in FILE_1
FILE_1_UNIQ=${FILE_1}-uniq
echo -n "" > ${FILE_1_UNIQ}
IFS=$'\n'
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

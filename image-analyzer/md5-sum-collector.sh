if [[ -z $1 ]]; then
    echo "no path for analyzing"
    exit 1
fi
if [[ -z $2 ]]; then 
    echo "no output report file specified"
    exit 2
fi
touch $2
output_file_size=`ls -la files.psv | awk '{print $5}'`
if [[ $output_file_size != 0]]; then
    echo "output file is not empty "
    exit 3
fi

file_type=( gif jpeg jpg JPG png PNG )


for each_file in `find $1 `; do
    md5sum_result=`md5sum $each_file 2>/dev/null`
    if [[ -n $md5sum_result ]]; then
      	# echo "md5sum_result: $md5sum_result"
    	md5sum_value=`echo $md5sum_result | awk '{print $1}' `
    	file_name=`echo $each_file | awk -F '/' '{print $NF}' `
    	echo $md5sum_value"|"$file_name"|"$each_file
    fi
done


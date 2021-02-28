full_path=`realpath $1`
file_name="$(basename -- $full_path)"
file_name_without_ext=${file_name%.*}
file_name_svg=$file_name_without_ext".svg"
file_dir="$(dirname -- $full_path)"

docker run --volume $file_dir:/external -t automation4archi /bin/bash /root/export-to-svg.sh $file_name $file_name_svg

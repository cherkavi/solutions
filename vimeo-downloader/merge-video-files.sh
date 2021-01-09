output_line="init-video.mp4"
# for each_file in ls -v *.video.mp4
for each_file in $(ls -v *.video.mp4)
do
    output_line=$output_line" "$each_file
done
eval  "cat "$output_line" > video-full.mp4"
output_line="init-audio.mp4"
for each_file in $(ls -v *.audio.mp4)
do
    output_line=$output_line" "$each_file
done
eval  "cat "$output_line" > audio-full.mp4"
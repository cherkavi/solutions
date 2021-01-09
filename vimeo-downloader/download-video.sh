# 173715084
clip_id=`cat init.json | jq ". | .clip_id" | awk -F "\"" '{print $2}'`
# 561762299
base_url=`cat init.json | jq ". | .video[0].base_url" | awk -F "\"" '{print $2}'`
# 173715084/sep/audio/561762299/chop/
url_suffix="$clip_id/sep/video/$base_url"

cat init.json | jq ". | .video[0].segments[].url" | awk -F "\"" '{print $2}' | while read each_file
do
    eval "curl "$prefix$url_suffix$each_file"  --output "$each_file".video.mp4"
done

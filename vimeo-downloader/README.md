## copy init url 
```sh
# expected: https://85vod-adaptive.akamaized.net/exp=1610185~acl=%2F173715%2F%2A~hmac=d56f3fbdeb36d036c3d309fce220d02e71cd2d05ca3ee3d7f0/173715084/sep/video/561762299,561762298/master.json?base64_init=1
init_url=`cat init_url.txt`
echo $init_url

## download init.json
curl $init_url --output init.json

## make remote url
export prefix=`echo $init_url | awk -F '/' '{print $1"/"$2"/"$3"/"$4"/"}'` 
echo $prefix

## make init frames
./make-init-video.sh
ls init-video.mp4
./make-init-audio.sh
ls init-audio.mp4

## download parts
./download-video.sh
./download-audio.sh

## merging
# make video.mp4
./merge-video-files.sh
rm *video.mp4
# rifle video-full.mp4

# make audio.mp4
./merge-audio-files.sh
rm *audio.mp4
# rifle video-full.mp4

## fusion 
ffmpeg -i video-full.mp4 -i audio-full.mp4 output.mp4
rm video-full.mp4
rm audio-full.mp4
rm init.json
rm *video.mp4
rm *audio.mp4
rifle output.mp4
```
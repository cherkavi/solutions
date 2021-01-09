## copy init url 
```sh
init_url='https://85vod-adaptive.akamaized.net/exp=1610185~acl=%2F173715%2F%2A~hmac=d56f3fbdeb36d036c3d309fce220d02e71cd2d05ca3ee3d7f0/173715084/sep/video/561762299,561762298/master.json?base64_init=1'
```

## download init.json
```sh
curl $init_url --output init.json
```

## make remote url
```sh
prefix=`echo $init_url | awk -F '/' '{print $1"//"$2"/"$3"/"$4"/"}'` 
echo $prefix
```

## download parts
```sh
# download it
# eval
./print-url-video.sh
./print-url-audio.sh
```

## merging
```sh
# make video.mp4

# make audio.mp4

```

## fusion 
```
ffmpeg -i video.mp4 -i audio.mp4 output.mp4
```
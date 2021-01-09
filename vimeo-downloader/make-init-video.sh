cat init.json | jq ". | .video[0].init_segment" | awk -F "\"" '{print $2}' | base64 --decode > init-video.mp4

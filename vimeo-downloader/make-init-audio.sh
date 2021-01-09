cat init.json | jq ". | .audio[0].init_segment" | awk -F "\"" '{print $2}' | base64 --decode > init-audio.mp4

# script for printing everything in folder and remove file afterward
> comfortable for making photo, send to Dropbox/FTP, obtain from printer 

## Architecture
![2023-04-14 17-23_Seite_1](https://user-images.githubusercontent.com/8113355/232087878-6ec2d0c7-5337-4544-a288-aa108d3ae11e.jpg)


## run current script in destination folder
```sh
## select one of the printer by name
# lpstat -l -v
PRINTER_NAME=HLL8260CDW

while true; do
    ## today's created files in the folder
    # for each_file in `find . -type f -name "*.jpg" -daystart -ctime 0`; do

    ## list of all files in the folder with jpg extension
    for each_file in `ls *.jpg`; do
        out_file=out.jpg
        convert $each_file -resize 200 -rotate -90 -contrast $out_file
        lpr -P $PRINTER_NAME -o fit-to-page=false -o position=top $out_file
        sleep 2
        rm $out_file
        rm $each_file
    done 
    sleep 5
done;
```

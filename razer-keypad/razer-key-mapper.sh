################################################
### key mapper for razer device              ###
### * first argument - path to file with map ###
################################################
#
# /home/projects/solutions/razer-keypad/razer-key-mapper.sh /home/projects/solutions/razer-keypad/razer-tartarus-sketchtogether.hwdb
# /home/projects/solutions/razer-keypad/razer-key-mapper.sh /home/projects/solutions/razer-keypad/razer-tartarus-ksnip.hwdb
# /home/projects/solutions/razer-keypad/razer-key-mapper.sh /home/projects/solutions/razer-keypad/razer-tartarus-visual-paradigm.hwdb
# 
if test -z "$1"; then
    echo "no input file - select one from current folder"
    exit 1
fi
DESTINATION_NAME="90-keypad-custom.hwdb"
DESTINATION_PATH="/etc/udev/hwdb.d/"$DESTINATION_NAME

EXISTING_MD5_SUM=`md5sum $DESTINATION_PATH | cut --delimiter=' ' --fields=1`
TARGET_MD5_SUM=`md5sum $1 | cut --delimiter=' ' --fields=1`

if [ $EXISTING_MD5_SUM != $TARGET_MD5_SUM ]; then
    # "need to replace"
    sudo cp $1 $DESTINATION_PATH
    sudo udevadm hwdb --update
    sudo udevadm trigger --sysname-match="event*"
else
    echo "already applied"
fi
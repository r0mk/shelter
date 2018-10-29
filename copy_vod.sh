#!/bin/bash
UPLOAD="/home/vod"   #FOLDER FOR STREAM SERVER (CHANGE TO YOUR PATH)
DESTINATION="54.39.106.158:/home/vod/"
HISTORY="/home/ppv_folder_tmp"   #FOLDER FOR MARK FILES (CHANGE TO YOUR PATH)
RANDOM_FILE=`(ls -t  $UPLOAD/*.mp4 | shuf -n1)` # Random file from uploadTO YOUR PATH)
echo $RANDOM_FILE
[ ! -d  $PLAY_LIST ] && mkdir $PLAY_LIST
[ ! -d  $HISTORY ] && mkdir $HISTORY
#r0mk
#Remove old files from history
find $HISTORY -mtime +7 -exec rm -f {} \;
#r0mk
counter=1
copied=1
while true; do
    RANDOM_FILE="`(ls $UPLOAD -tr | grep mp4|  tail -n $counter | head -n 1)`"
    if [ -e "$HISTORY/$RANDOM_FILE" ] || [ ! -f "$UPLOAD/$RANDOM_FILE" ]; then
    echo "Not fit to us $HISTORY/$RANDOM_FILE"
    counter=$((counter + 1))
    echo $counter
    else
    if [ `ffprobe -i  $UPLOAD/$RANDOM_FILE -show_format -v quiet  | grep format_name | grep 'mp4'` ]; then
        echo "New will be $UPLOAD/$RANDOM_FILE"
        touch "$HISTORY/$RANDOM_FILE"
        scp "$UPLOAD/$RANDOM_FILE" "$DESTINATION`echo "$RANDOM_FILE" | tr ' ' '_' | tr ',' '_' | tr '-' '_'`"
        echo "Copied $copied"
        copied=$((copied + 1))
    else
        echo "Wrong encoding $UPLOAD/$RANDOM_FILE"
        touch "$HISTORY/$RANDOM_FILE"
    fi
    fi
    if [ $counter -ge 300 ]; then
        echo "No suitable file found. Does not to copy. exit"
        break
    fi
    if [ $copied -ge 11 ]; then
        echo "I am copy 10 files. Enough for today. exit"
        break
    fi
done

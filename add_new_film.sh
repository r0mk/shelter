#!/bin/bash
PLAY_LIST="/home/ppv_folder"
UPLOAD="/home/main_source"   #FOLDER FOR STREAM SERVER (CHANGE TO YOUR PATH)
HISTORY="/home/ppv_folder_tmp"   #FOLDER FOR MARK FILES (CHANGE TO YOUR PATH)
RANDOM_FILE=`(ls -t  $UPLOAD | shuf -n1)` # Random file from uploadTO YOUR PATH)

find $HISTORY -mtime +22 -exec rm -f {} \;
counter=1
while true; do
    RANDOM_FILE=`(ls $UPLOAD -t |  tail -n $counter | head -n 1)`
    if [ -e "$HISTORY/$RANDOM_FILE" ]; then
    echo "Not fit to us $HISTORY/$RANDOM_FILE"
    counter=$((counter + 1))
    echo $counter
    else
        echo "New will be $UPLOAD/$RANDOM_FILE"
        touch "$HISTORY/$RANDOM_FILE" 
        #echo "$PLAY_LIST/\* -f"
        rm $PLAY_LIST/*
        cp "$UPLOAD/$RANDOM_FILE" $PLAY_LIST/`echo "$RANDOM_FILE" | tr ' ' '_' | tr ',' '_' | tr '-' '_'`
        break 
    fi
    if [ $counter -ge 300 ]; then
        echo "No suitable file found. Does not to copy. exit" 
        break
    fi
done

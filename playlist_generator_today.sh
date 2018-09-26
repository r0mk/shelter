#!/bin/bash
PLAY_LIST="/home/playlist.txt"
HISTORY="/home/playlist_tmp"   #FOLDER FOR MARK FILES (CHANGE TO YOUR PATH)
UPLOAD="/home/vod"   #FOLDER FOR STREAM SERVER (CHANGE TO YOUR PATH)
[ ! -d  $HISTORY ] && mkdir $HISTORY

Today=`date -d "today" +"%Y-%m-%d"`
Today_unix=`date +%s -d\`date -d "today" +"%Y-%m-%d"\``
Tomorrow=`date -d "1 days" +"%Y-%m-%d"`
Tomorrow_unix=`date +%s -d\`date -d "1 days" +"%Y-%m-%d"\``
echo "Today $Today"
echo "Today unix $Today_unix"
echo "Tomorrow $Tomorrow"
echo "Tomorrow unix $Tomorrow_unix"


echo "" >  $PLAY_LIST
echo -e "\n\n\n"
find $HISTORY -mtime +7 -exec rm -f {} \;
time="$Today_unix"
counter=1
while true; do
    RANDOM_FILE=`(ls $UPLOAD -tr |  tail -n $counter | head -n 1)`
    if [ -e "$HISTORY/$RANDOM_FILE" ]; then
    #echo "Not fit to us $HISTORY/$RANDOM_FILE"
    counter=$((counter + 1))
    #echo $counter
    else
        #echo "New will  be added $UPLOAD/$RANDOM_FILE"
        touch "$HISTORY/$RANDOM_FILE"
        echo -e "#EXT-X-UTC:$time\nPPV_FULL/vod/$RANDOM_FILE"
        echo -e "#EXT-X-UTC:$time\nPPV_FULL/vod/$RANDOM_FILE" >> $PLAY_LIST
        #lenght=printf '%.0f\n' `ffprobe -i  $UPLOAD/$RANDOM_FILE -show_format -v quiet | sed -n 's/duration=//p'`
        lenght="`ffprobe -i  $UPLOAD/$RANDOM_FILE -show_format -v quiet | sed -n 's/duration=//p'`"
        round_lenght="`printf '%.0f\n' $lenght`" 
        #echo "lenght $lenght"
        #echo "round lenght $round_lenght"
        time=$(($time + round_lenght))
        
    fi
    if [ $counter -ge 400 ]; then 
        echo "No suitable file found. Playlist no full. exit"
        break
    fi
    if [ $time -ge $Tomorrow_unix ]; then
        echo -e "Playlist for today generated. \n You may take it $PLAY_LIST"
        break
    fi

done


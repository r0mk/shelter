#!/bin/bash
PLAY_LIST="/home/XML_and_playlist.txt"
XML_epg="/home/XML_epg.xml"
HISTORY="/home/playlist_tmp"   #FOLDER FOR MARK FILES (CHANGE TO YOUR PATH)
UPLOAD="/home/vod"   #FOLDER FOR STREAM SERVER (CHANGE TO YOUR PATH)
CHANNEL_NAME='Best vod Movies'
[ ! -d  $HISTORY ] && mkdir $HISTORY
Tomorrow=`date -d "tomorrow" +"%Y-%m-%d"`
Tomorrow_unix=`date +%s -d\`date -d "tomorrow" +"%Y-%m-%d"\``
DayAfterTomorrow=`date -d "2 days" +"%Y-%m-%d"`
DayAfterTomorrow_unix=`date +%s -d\`date -d "2 days" +"%Y-%m-%d"\``
echo "Tomorrow $Tomorrow"
echo "Tomorrow unix $Tomorrow_unix"
echo "Day after tomorrow $DayAfterTomorrow"
echo "Day after tomorrow unix $DayAfterTomorrow_unix"
#Header for XML
echo "" > $PLAY_LIST
rm -f $XML_epg
echo  "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" >> $XML_epg

echo  -e "<tv generator-info-name=\"WebGrab+Plus/w MDB & REX Postprocess -- version  V2.1 -- Jan van Straaten\" generator-info-url=\"http://www.webgrabplus.com\">\n <channel id=\"$CHANNEL_NAME\">\n  <display-name lang=\"en\">$CHANNEL_NAME</display-name>\n </channel>" >> $XML_epg
echo -e "\n\n\n" 
#Clear history
find $HISTORY -mtime +7 -exec rm -f {} \;
time="$Tomorrow_unix"
counter=1
while true; do
    RANDOM_FILE=`(ls $UPLOAD -tr |  tail -n $counter | head -n 1)`
    FOR_TITLE=`echo ${RANDOM_FILE%.*} | sed 's/\./ /g' | sed 's/\_/ /g' | awk '{print toupper($0)}'`
    if [ -e "$HISTORY/$RANDOM_FILE" ]; then
    echo "Not fit to us $HISTORY/$RANDOM_FILE"
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
        echo -en " <programme start=\"`date  +\"%Y%m%d%H%M00\" -d\"@$time\"` -0500\" " >> $XML_epg
        time=$(($time + round_lenght))
        echo "stop=\"`date  +\"%Y%m%d%H%M00\" -d\"@$time\"` -0500\" channel=\"$CHANNEL_NAME\">" >> $XML_epg
        echo -e "  <title lang=\"en\">$FOR_TITLE</title>\n </programme>" >> $XML_epg

    fi
    if [ $counter -ge 400 ]; then
        echo "No suitable file found. Playlist no full. exit"
        break
    fi
    if [ $time -ge $DayAfterTomorrow_unix ]; then
        echo -e "Playlist for tomorrow generated. You man take it $PLAY_LIST"
        echo -e "EPG generated too. You man take it $XML_epg"
        echo "</tv>" >> $XML_epg
        break
    fi

done


#!/bin/bash
#This script uses to calculate all mp3's lenth
DIRECTORY=$1

round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

lenth=0
find $DIRECTORY -name '*.mp3' | while read file; do echo "file $file"; lenth=`ffprobe -i  "$file" -show_format -v quiet | sed -n 's/duration=//p'`; lenth=$(round $lenth 0); summary_lenth=$((summary_lenth + $lenth)); echo -e "file lenth = $lenth \n summary = $summary_lenth \n\n" ; done

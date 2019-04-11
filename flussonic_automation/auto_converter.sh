INPUT_FOLDER=/root/for_convertation
OUTPUT_FOLDER=/root/converted

pathname="$1"
extension=${pathname##*.}
filename=${pathname##*/}
echo $extension
if [ $extension == "mkv" ]; then 
    echo "$filename it mkv, will be converted to mp4"
    echo "ffmpeg -i $pathname -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 192k -ac 2 /root/converted/$filename.mp4"
    ffmpeg -i "$pathname" -c:v libx264 -crf 26 -preset slow -c:a aac -b:a 192k -ac 2 /root/converted/$filename.mp4
fi


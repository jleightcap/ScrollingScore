#!/bin/bash

###########
# OPTIONS #
###########
IMGS="./Sheets"
OUT="output.mp4"
TIME_DATA="times.txt"
FPS=25



#############
# SCRIPTING #
#############
FILES=`find $IMGS/*.png`

# Manually count images in $IMGS
let IMG_COUNT=0
for _ in ${FILES[@]}; do (( IMG_COUNT+=1 )); done
IMG_COUNT=$((IMG_COUNT-1))

# Start $FULL_SCRIPT, the eventual string to be eval'd.
# Import images directory
FULL_SCRIPT="ffmpeg -i $IMGS/%3d.png "
# Import audio, argv[1]
FULL_SCRIPT+="-i $1 "

# Read absolute time data 
declare -a TIMES
while read line; do
  # ignore commented lines
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  # convert "HH:MM:SS" -> seconds
  # these times are absolute
  TIMES+=($(echo $line | awk -F: '{print($1*3600)+($2*60)+$3}'))
done < $TIME_DATA

# Convert times into relative lengths based on previous timestamp
TIMES_RELATIVE=(${TIMES[0]})
for (( ii=1; ii<${#TIMES[@]}; ii++ )); do
  TIMES_RELATIVE+=($((${TIMES[$ii]} - ${TIMES[$ii - 1]})))
done

FRAME_COEF=""
for (( ii=0; ii<$IMG_COUNT; ii++ )); do
  FRAME_COEF+="'$((${TIMES_RELATIVE[$ii]}*$FPS))*eq(in,$ii)'+";
done
FRAME_COEF+="'$((${TIMES_RELATIVE[$IMG_COUNT]}*$FPS))*eq(in,$IMG_COUNT)'"

FULL_SCRIPT+="-vf \"zoompan=d=$FRAME_COEF\" "
FULL_SCRIPT+=$OUT

echo $FULL_SCRIPT
eval ${FULL_SCRIPT}
unset -v FRAMES

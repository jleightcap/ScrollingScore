#!/bin/bash

###########
# OPTIONS #
###########
FPS=60
IMGS="./Sheets"
OUT="test.mp4"
FRAMES_DATA="frames.txt"



#############
# SCRIPTING #
#############
FILES=`find $IMGS/*.png`

# Manually count images in $IMGS
let IMG_COUNT=0
for _ in ${FILES[@]}; do (( IMG_COUNT+=1 )); done

# Start $FULL_SCRIPT, the eventual string to be eval'd.
# Import images directory
FULL_SCRIPT="ffmpeg -i $IMGS/%3d.png "
# Import audio, argv[1]
FULL_SCRIPT+="-i $1 "

# Read frame data 
declare -a FRAMES
while read line; do
  [[ "$line" =~ ^[[:space:]]*# ]] && continue
  FRAMES+=($line)
done < $FRAMES_DATA

FRAME_COEF=""
for (( ii=0; ii<$IMG_COUNT-1; ii++ )) do
  FRAME_COEF+="'${FRAMES[$ii]}*eq(in,$ii)'+";
done
FRAME_COEF+="'50*eq(in,$IMG_COUNT)'"

FULL_SCRIPT+="-vf \"zoompan=d=$FRAME_COEF\" "
FULL_SCRIPT+=$OUT

echo $FULL_SCRIPT
eval ${FULL_SCRIPT}
unset -v FRAMES

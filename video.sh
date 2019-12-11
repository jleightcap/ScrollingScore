#!/bin/bash

###########
# OPTIONS #
###########
FPS=60
IMGS="./Sheets"
OUT="test.mp4"


#############
# SCRIPTING #
#############
FILES=`find $IMGS/*.png`
# import images directory
FULL_SCRIPT="ffmpeg -i $IMGS/%3d.png "
# import audio, argv[1]
FULL_SCRIPT+="-i $1 "
# timing
FULL_SCRIPT+="-vf \"zoompan=d=25\" "
#+'50*eq(in,1)\" "
FULL_SCRIPT+=$OUT

echo $FULL_SCRIPT
eval ${FULL_SCRIPT}

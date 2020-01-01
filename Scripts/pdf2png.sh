#!/bin/bash

mkdir Output
cd Output
gs -dNOPAUSE -sCompression=none -dBATCH -sDEVICE=png16m -sOutputFile="Page-%d.png" ../$1

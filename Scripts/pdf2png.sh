#!/bin/bash

mkdir Output
cd Output
gs -dNOPAUSE -dBATCH -sDEVICE=png16m -sOutputFile="Page-%d.png" ../$1

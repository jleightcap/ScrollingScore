#!/bin/bash

pdftk "$@" cat output Sum.pdf

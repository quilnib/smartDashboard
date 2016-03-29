#!/bin/sh

export DISPLAY=:0.0

tvservice -e "DMT 87 DVI" # this is specificially for the 5" screen
# add this back in for normal monitors tvservice --preferred
sleep 1
fbset -depth 8
fbset -depth 16
xrefresh

#!/bin/sh

tvservice -e "DMT 87 DVI" # this is specificially for the 5" screen
# add this back in for normal monitors tvservice --preferred
fbset -depth 8
fbset -depth 16
xrefresh

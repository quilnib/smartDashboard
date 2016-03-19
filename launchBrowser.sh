#! /bin/sh


export DISPLAY=:0.0
epiphany-browser -a --profile ~/.config dashboard.classictim.com --display=:0.0 &
sleep 10s;
xte "key F11" -x:0.0

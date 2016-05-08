import subprocess
import time
import RPi.GPIO as io
io.setmode(io.BCM)

pir_pin = 18
relay_pin = 23
io.setup(pir_pin, io.IN)
io.setup(relay_pin, io.OUT)
io.output(relay_pin, False)

lastMotionTime = time.time()
lastRefreshTime = time.time()
refreshCounter = 0
refreshInterval = 300 #refresh every 5 minutes
sleepInterval = 10 #turn the screen off after 10-seconds of inactivity

def main():
    global lastMotionTime
    global lastRefreshTime
    global refreshCounter

    setDisplay()
    launchBrowser()

    time.sleep(10.0)#let the browser finish launching before checking for activity
    while True:
        if io.input(pir_pin):
            print("The infrared sensor was triggered")
            lastMotionTime = time.time()
            refreshCounter += 1
            #if the screen is off, turn it on
            wakeScreen()
            if (refreshCounter > refreshInterval):
                refreshScreen()
            #if the screen has been on for more than 5-minutes, refresh
            #if (lastRefreshTime + refreshInterval) < time.time():
                #refreshScreen()
                #lastRefreshTime = time.time()
        else:
            print("no movement registered")
            #if the screen is on, and there has been no activity for a period of time, turn off screen
            if (lastMotionTime + sleepInterval)< time.time(): # and isMonitorRunning():
                sleepScreen()
        time.sleep(1.0)


def launchBrowser():
    #setDisplay()    
    subprocess.call("bash /home/pi/Documents/smartDashboard/launchBrowser.sh", shell=True)

def wakeScreen():
    print("waking screen")
    io.output(relay_pin, False)#the logic is inverted for some reason...

def sleepScreen():
    global refreshCounter
    print("sleeping screen")
    refreshCounter = 0
    io.output(relay_pin, True)

def refreshScreen():
    global lastRefreshTime
    global refreshCounter
    subprocess.call("xte 'key F5'", shell=True)
    lastRefreshTime = time.time()
    refreshCounter = 0

def setDisplay():
    subprocess.call("export DISPLAY=:0.0", shell=True)

if __name__ == '__main__':
    main()


import subprocess
import time
import RPi.GPIO as io
io.setmode(io.BCM)

pir_pin = 18
io.setup(pir_pin, io.IN)

lastMotionTime = time.time()
lastRefreshTime = time.time()
refreshInterval = 300 #refresh every 5 minutes
sleepInterval = 30 #turn the screen off after 30-seconds of inactivity

def main():
    global lastMotionTime
    global lastRefreshTime

    setDisplay()
    launchBrowser()

    time.sleep(10.0)#let the browser finish launching before checking for activity
    while True:
        if io.input(pir_pin):
            print("The infrared sensor was triggered")
            lastMotionTime = time.time()
            #if the screen is off, turn it on
            if not isMonitorRunning():
                wakeScreen()
            #if the screen has been on for more than 5-minutes, refresh
            if (lastRefreshTime + refreshInterval) < time.time():
                refreshScreen()
                #lastRefreshTime = time.time()
        else:
            print("no movement registered")
            #if the screen is on, and there has been no activity for a period of time, turn off screen
            if (lastMotionTime + sleepInterval)< time.time() and isMonitorRunning():
                sleepScreen()
        time.sleep(5.0)


def launchBrowser():
    setDisplay()    
    subprocess.call("bash /home/pi/Documents/smartDashboard/launchBrowser.sh", shell=True)

def isMonitorRunning():
    status = subprocess.check_output("tvservice -s", shell=True).decode("utf-8")

    if "TV is off" in status:  #check for a chunk of string specific to the "off" status of the screen
        return False
    else:
        return True

def wakeScreen():
    print("waking screen")
    setDisplay()
    subprocess.call("bash /home/pi/Documents/smartDashboard/wakeMonitor.sh", shell=True)

def sleepScreen():
    print("sleeping screen")
    setDisplay()
    subprocess.call("bash /home/pi/Documents/smartDashboard/sleepMonitor.sh", shell=True)

def refreshScreen():
    global lastRefreshTime
    subprocess.call("xte 'key F5'", shell=True)
    lastRefreshTime = time.time()

def setDisplay():
    subprocess.call("export DISPLAY=:0.0", shell=True)

if __name__ == '__main__':
    main()



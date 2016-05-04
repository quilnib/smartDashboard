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
refreshInterval = 300 #refresh every 5 minutes
sleepInterval = 10 #turn the screen off after 10-seconds of inactivity

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
            #if not isMonitorRunning():
                #wakeScreen()
            wakeScreen()
            #if the screen has been on for more than 5-minutes, refresh
            #if (lastRefreshTime + refreshInterval) < time.time():
            #    refreshScreen()
                #lastRefreshTime = time.time()
        else:
            print("no movement registered")
            #if the screen is on, and there has been no activity for a period of time, turn off screen
            if (lastMotionTime + sleepInterval)< time.time() and isMonitorRunning():
                sleepScreen()
        time.sleep(1.0)


def launchBrowser():
    #setDisplay()    
    subprocess.call("bash /home/pi/Documents/smartDashboard/launchBrowser.sh", shell=True)

def isMonitorRunning():  #the references to this have been commented out since the Mosfet has been connected
    status = subprocess.check_output("tvservice -s", shell=True).decode("utf-8")

    if "TV is off" in status:  #check for a chunk of string specific to the "off" status of the screen
        return False
    else:
        return True

def wakeScreen():
    print("waking screen")
    #setDisplay()
    #subprocess.call("bash /home/pi/Documents/smartDashboard/wakeMonitor.sh", shell=True)
    io.output(relay_pin, True)

def sleepScreen():
    print("sleeping screen")
    #setDisplay()
    #subprocess.call("bash /home/pi/Documents/smartDashboard/sleepMonitor.sh", shell=True)
    io.output(relay_pin, False)

def refreshScreen():
    global lastRefreshTime
    subprocess.call("xte 'key F5'", shell=True)
    lastRefreshTime = time.time()

def setDisplay():
    subprocess.call("export DISPLAY=:0.0", shell=True)

if __name__ == '__main__':
    main()


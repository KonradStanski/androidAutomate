# SAMPLE AUTOMATION SCRIPT
from androidAutomateAPI import Device
import time

# Argument is determined from `adb devices` command. In this case it is a Samsung s9
# myDevice = Device("384852514b573398") #s9
myDevice = Device("0283548d344b7a24") #nexus



myDevice.wakeup()
myDevice.launchApp("com.instagram.android")

myDevice.inputSwipe(10, 90, 90, 90, percent=True)

myDevice.tapNode("LIVE")
myDevice.tapNode("Go Live")

# Do a little broadcast
time.sleep(20)

myDevice.tapNode("End")
myDevice.tapNode("End Live Video")
myDevice.closeApp("com.instagram.android")
myDevice.sleep()

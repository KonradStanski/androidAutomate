# SAMPLE AUTOMATION SCRIPT
from androidAutomateAPI import Device
import time

# Argument is determined from `adb devices` command. In this case it is a Samsung s9
myDevice = Device("384852514b573398")

myDevice.inputSwipe(500, 800, 500, 400) #This represents a swipe up
myDevice.inputSwipe(500, 800, 500, 400, 1000) #This represents a swipe up but slow
myDevice.inputSwipe(50, 20, 50, 80, percent=True) #This represents a swipe up but with the x and y inputs being a percentage
time.sleep(0.2)



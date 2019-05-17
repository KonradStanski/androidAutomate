from androidAutomateAPI import Device
import time

# Argument is determined from `adb devices` command. In this case it is a Samsung s5
myDevice = Device("0283548d344b7a24")

# Wake Phone screen
myDevice.wakeup()

# Search for the youtube app
myDevice.searchApp("youtube")

# Using the name found, launch the youtube app
myDevice.launchApp("com.google.android.youtube")

# Wait for app to load
time.sleep(2)

# swipe up a couple times to browse videos
for i in range(4):
	myDevice.inputSwipe(500, 1300, 500, 400)
	time.sleep(0.2)

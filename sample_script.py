from androidAutomateAPI import Device
import time
# Argument is determined from `adb devices` command. In this case it is a Samsung s5
s5 = Device("97342cf1")

# Search for the intagram app
s5.searchApp("insta")

# Using the name found, launch the instagram app
s5.launchApp("com.instagram.android")

# Wait for app to load
time.sleep(2)

# swipe to get into the camera
s5.inputSwipe(0, 1000, 1000, 1000)
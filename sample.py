# SAMPLE AUTOMATION SCRIPT
from androidAutomateAPI import Device
import time

# Argument is determined from `adb devices` command. In this case it is a Samsung s9
myDevice = Device("384852514b573398")

# myDevice.launchApp("com.android.settings")

# Wait for app to load / **REPLACE WITH FUNCTION TO DETECT WHEN APP LOADS** /
# time.sleep(2)


myDevice.tapNode("Search")

myDevice.inputText("test")
# androidAutomate:
## What Is It?
- Android Automate is a root-less android automation tool
-
- Provides an easy to use python based object oriented API for injecting ADB commands to your android devices
-

## Table of Contents
- [Getting Started](#getting-started)
- [Quick Use Guide](#quick-use-guide)
- [Api Usage](#api-usage)


## Getting Started
In order to use this tool you will need:

- Install ADB on your machine.
	- You can do this by running `sudo apt-get install adb` on debian systems or `sudo dnf install adb` on rpm system. Check if this worked by running: `adb devices`
- Enable USB debugging on your android phone.
	- This can be acheived on most models by opening the settings menu on your phone, navigating to "about phone" or "system information". Find "Build Number" and tap on it 7-10 times. This will enable developer options. Navigate back to the setting menu, and open the developer options. From here you may enable USB debugging.
	- Verify this worked by running `adb devices`. You should see your device listed as: `<deviceId> device`


## Quick CLI Use Guide

How to Record Events

How to Playback Events


## API Reference




```python
import androidAutomate.py
```



### Change Log
V1.0:
	Basic funcionality is present


### Things To Fix/ Add
- proper object oriented class structure for api
- a device object that stores information about the connected device
- the ability to click relative positions on the screen wrt the size of the screen



<!-- adb shell wm density gets density
adb shell wm size gets screen size
 -->

<!-- openApp = "adb shell monkey -p com.whatsapp -v 1"



record = "adb shell getevent -t /dev/input/event1 > recorded_touch_events.txt"

setup = "adb push mysendevent /data/local/tmp/"
sendToPhone = "adb push recorded_touch_events.txt /sdcard/"
playback = "adb shell /data/local/tmp/mysendevent /dev/input/event1 /sdcard/recorded_touch_events.txt"



adb -s emulator-5554 shell input swipe 1040 1422 125 1422
adb  shell pm list packages
adb shell getevent -l
adb -s 0283548d344b7a24 shell sendevent




adb shell getevent -t /dev/input/event1 > recorded_touch_events
adb push mysendevent /data/local/tmp/
adb push recorded_touch_events /sdcard/
adb shell /data/local/tmp/mysendevent /dev/input/event1 /sdcard/recorded_touch_events
 -->
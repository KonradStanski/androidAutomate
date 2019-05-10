# androidAutomate:
##Terminal Utility for recording, playing, and chaining together android actions and gestures

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Setup Guide](#quick-setup-guide)
- [Api Usage](#api-usage)


## Prerequisites
In order to use this tool you will need:

- Install ADB on your machine. you can do this by running `sudo apt-get install adb` on debian systems or `sudo dnf install adb` on rpm system. Check if this worked by running: `adb devices`
- Enable usb debugging on your android phone. This can be acheived on most models by


## Quick Setup Guide

### How to Record Events

### How to Playback Events

### How to

## API Usage




```python
import androidAutomate.py
```



### Change Log
V1.0:
	Basic funcionality is present









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
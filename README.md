# androidAutomate:
## What Is It?
- Android Automate is a root-less android automation tool.
- Allows for touch recording and playback.
- Provides an easy to use python object oriented API for injecting ADB commands to your android devices.
- Allows for chaining common tasks together in the CLI interface.
- Can be used for automating Unit and Regression testing.
- Because this utility uses ADB, it is possible to automate AVD, emulator, and real android devices.




## Table of Contents
- [Getting Started](#getting-started)
- [Quick CLI Use Guide](#quick-cli-use-guide)
- [Writing Scripts](#writing-scripts)
- [Api Reference](#api-reference)
- [Debugging FAQ](#debgging-faq)




## Getting Started
In order to use this tool you will need to:

- Install **python 3.7** (Need atleast Python 3.6 for f-strings)

- Install **ADB** on your machine.
	- You can do this by running `sudo apt-get install adb` on debian systems or `sudo dnf install adb` on an rpm system. Check if this worked by running: `adb --version`
- Enable **USB debugging** on your android phone.
	- This can be acheived on most models by opening the settings menu on your phone, navigating to "about phone" or "system information". Find "Build Number" and tap on it 7-10 times. This will enable developer options. Navigate back to the setting menu, and open the developer options. From here you may enable USB debugging.
	- Verify this worked correctly by running `adb devices`. You should see your device listed as: `<deviceId> device`
		- If it does not show anything then most likely have to install your device's USB drivers for linux.
		- If it shows `<deviceId> unauthorized` make sure to connect the phone and tap ok on the popup asking you for permission to allow usb debugging.

- Only tested on linux systems. May not work on Windows as it uses UNIX style OS calls.




## Quick CLI Use Guide
- Run androidAutomate.py with `python3 androidAutomate.py`
- Choose your device from the list

#### How to Record Events:
- Choose Record Event
- Provide a name for the event i.e: "send snapchat"
- perform the action on the device
- Press CTRL-C to stop recording
- The event is now stored in ./events and can be viewed and edited. To format of storing touch events is up for change

#### How to Playback Events:
- Choose Playback Event
- provide the name of the event i.e: "send sbnapchat"
- make sure the device is in the same state as when you recorded the event
- The event will now play

#### How to create Chains:
- Choose Create Chain
- Provide a name for the chain
- Choose which action you would like to start and follow the instructions
- Make sure to choose the exit option when you are done
- You can go into ./chains and edit the chains manualy if you wish.

#### How to play Chains:
- Choose Playback Chain
- Type the name of the chain you would like to play
- Make sure the device is in the same state as what is expected from the first event in the Chain
- The chain will now play

#### Searching for an app:
- Choose Search Application
- Provide a search criteria term like you would with grep (it's using grep on the output of the list applications output)




## Writing Scripts
This module provides the option of importing the main androidAutomate.py file to programmatically control your automation task.
This is an example script where the deviceId is passed during the instanciation of the device. The deviceId can be determined from the command `adb devices`
```python
from androidAutomateAPI import Device
import time
# Argument is determined from `adb devices` command. In this case it is a Samsung s5
myDevice = Device("0283548d344b7a24")

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
```

## API Reference





## Debugging FAQ

**1.**
	A common issue is that the `detEventId()` method incorrectly identifies some other hardware device on your mobile device as being the touchscreen. If this is the case, you will have to manually check the eventId for touch getures.
	run: `adb shell getevent -lp` and find the touchscreen.
	**ex output to adb shell getevent -lp:**
```bash
add device 9: /dev/input/event2 <-- ###THIS IS THE NUMBER YOU WANT###
	name:     "sec_touchscreen"
	events:
		KEY (0001): KEY_HOMEPAGE          BTN_TOOL_FINGER       BTN_TOUCH       01c7		02be
		ABS (0003): ABS_X                 : value 0, min 0, max 4095, fuzz 0, flat 0, resolution 0
					ABS_Y                 : value 0, min 0, max 4095, fuzz 0, flat 0, resolution 0
            		ABS_MT_SLOT           : value 0, min 0, max 9, fuzz 0, flat 0, resolution 0
	                ABS_MT_TOUCH_MAJOR    : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
	                ABS_MT_TOUCH_MINOR    : value 0, min 0, max 255, fuzz 0, flat 0, resolution 0
	                ABS_MT_POSITION_X     : value 0, min 0, max 4095, fuzz 0, flat 0, resolution 0
	                ABS_MT_POSITION_Y     : value 0, min 0, max 4095, fuzz 0, flat 0, resolution 0
	                ABS_MT_TRACKING_ID    : value 0, min 0, max 65535, fuzz 0, flat 0, resolution 0
	                003e                  : value 0, min 0, max -1, fuzz 0, flat 0, resolution 0
	    SW  (0005): 0020*
```
Set device.eventId to the eventId in /dev/input/event<eventId>. In this case it is 2. This can be achieved with: `device.eventId = <deviceId>`

**2.**
	If your device is **not showing up** in the `adb devices` command, look here for more info:
	https://stackoverflow.com/questions/21170392/android-device-does-not-show-up-in-adb-list/21470729
	https://forums.oneplus.com/threads/device-not-listing-using-adb-on-ubuntu-14-04-3.418957/
	https://stackoverflow.com/questions/32151114/adb-is-not-detecting-my-android-device-on-ubuntu

**3.**
	If your device shows up as **<deviceId> unauthorized** there are a couple things to check:
		USB debugging in developer options is checked
		Try running `adb kill-server` and then `adb start-server` after connecting your device. If you did not get a popup asking you if you trust usb debugging from this computer before, this should do it.



### TODO
- proper object oriented class structure for api []
- a device object that stores information about the connected device []
- the ability to click relative positions on the screen wrt the size of the screen []
- automatic event<#> detection []

### CHANGELOG
V1.0:
	Basic funcionality is present
	can record, replay, chain, and script basic things.

V1.1:





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
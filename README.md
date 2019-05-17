# Android Automate:
## What Is It?
- Android Automate is a root-less android automation tool.
- Allows for touch recording and playback.
- Provides an easy to use python object oriented API for injecting ADB commands to your android devices.
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

- Inorder to test if your device is recognized, it is highly recommended that under developer options, the "show touches" and "show swipes" options are enabled.


## Quick CLI Use Guide
- Run androidAutomate.py with `python3 androidAutomateCLI.py`
- Choose your device from the list

#### How to Record Events:
- Choose Record Event
- Provide a name for the event i.e: "send_snapchat"
- perform the action on the device
- Press CTRL-C to stop recording
- The event is now stored in ./events and can be viewed and edited. The format of storing touch events is up for review and may change

#### How to Playback Events:
- Choose Playback Event
- provide the name of the event i.e: "send_snapchat"
- make sure the device is in the same state as when you recorded the event
- The event will now play

#### Searching for an app:
- Choose Search Application
- Provide a search criteria term like you would with grep (Internaly it is just grep on the output of the list applications output)




## Writing Scripts
This module provides the option of importing the main androidAutomateAPI.py file to programmatically control your automation task.
This is an example script where the deviceId is passed during the instanciation of the device. The deviceId can be determined from the command `adb devices`
```python
# SAMPLE AUTOMATION SCRIPT
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
for i in range(4):      #x1   y1    x2   y2
    myDevice.inputSwipe(500, 1300, 500, 400)
    time.sleep(0.2)
```


## API Reference
```python
class Device():
"""
This is the class that allows all the other funcitons to be called.

Args:
	deviceID (str): The id of the device. Determined using `adb devices`
"""


def listEvents():
"""
Function that lists the contents of the /events/ folder
"""


def listChains():
"""
Function that lists to stdout the contents of the /chains/ folder
"""


def recordEvent(event):
"""
Function that records Touchscreen input until CTRL-C is typed into the terminal

Args:
	event (str): Name of file to which the event will be saved.
"""


def playEvent(event):
"""
Function that plays back a recorded event

Args:
	event (str): Name of the recorded file to play
"""


def playChain(chain):
"""
Function that plays a chain of events created in the CLI or manualy by editing a chain file

Args:
	chain (str): Name of the chain to play
"""


def listApps():
"""
Function that will list all of the installed packages on your device
"""


def searchApp(search):
"""
Function that allows you to search your device for an app. Returns the name of the app

Args:
	search (str): A search criteria that will grep through the output of the command
	`adb shell pm list packages`
"""


def launchApp(app):
"""
Function that launches an app

Args:
	app (str): Launches the supplied app. Apps may be listed in the CLI with listApps()
"""


def inputText(text):
"""
Function that inputs text without opening a keyboard on the phone

Args:
	text (str): Text to input
"""


def inputTap(x, y):
"""
Function that inputs a tap at the (x,y) coordinates provided. These can be viewed by turning on
the taps and swipes option in developer options

Args:
	x (int): x coordinate
	y (int): y coordinate
"""


def inputSwipe(x1, y1, x2, y2):
"""
Function that inputs a swipe starting at (x1, y1) and going to (x2, y2)

Args:
	x1 (int): x coordinate of beginning location of swipe
	y1 (int): y coordinate of beginning location of swipe
	x2 (int): x coordinate of end location of swipe
	y2 (int): y coordinate of end location of swipe
"""


def pressHome():
"""
Function that pressed the center home button on your device
"""


def pressBack():
"""
Function that pressed the back button on your device
"""


def pressPower():
"""
Function that presses the power button on your device
"""


def volumeUp():
"""
Function that presses the volume up button on your device
"""


def volumeDown():
"""
Function that presses the volume down button on your device
"""


def keycodeEvent(keycode):
"""
Function that inputs a keycode to the device. A reference list for keycodes can be
found in the /keycodes.txt file

Args:
	keycode (str/int): The string or integer description of the wanted keycode
"""
```


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
1. convert cli to class based API [X]
2. add a monkey runner function for random touch input []
3. automatic event<#> detection []
4. add screen width dependent input events []
5. convert openApp to open a fresh copy of the app every time [X]
6. record and replay input from all /dev/input/event# numbers and hardware devices []
7. proper object oriented class structure for API [X]
8. add availability to go to sepcific tasks within an app []


### CHANGELOG
V1.0:
	Basic funcionality is present
	can record, replay, chain, and script basic things.

V1.1:
	Converted to class based structure with python API
	Converted CLI to API
	Removed chains because they are redundant with scripts


### For other Developers and Contributors:
This module is essentialy a wrapper around the adb shell providing all the niceties of pythonic automation.
The replay of events is done by pushing the event record file to the sd card of the phone, then pushing the compiled executable file located in the ./src/ folder to the phone
The event is then played back from within the phone. This is done as doing the touch playback using python to input adb commands is simply too slow and produces unusable amounts of lag.
Currently this recording method only records the output from one device, but i believe it is simple enough to convert it to record
all of the devices of the phone, including the hardware buttons. That is on the todo list.




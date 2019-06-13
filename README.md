# Android Automate:
## What Is It?
- Android Automate is a root-less android automation tool.
- Allows for multi-touch recording and playback with accurate time replication.
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

- Install **python 3.7** (Need atleast Python 3.6 for f-strings).

- Install **ADB** on your machine.
	- You can do this by running `sudo apt-get install adb` on debian systems or `sudo dnf install adb` on an rpm system. Check if this worked by running: `adb --version`.
- For using emulators, [Android Studio](https://developer.android.com/studio) must be installed. You must then create an avd from the `tools/avdmanager` drop-down. Further information on how to do this can be found [here]()
- Enable **USB debugging** on your android phone.
	- This can be acheived on most models by opening the settings menu on your phone, navigating to "about phone" or "system information". Find "Build Number" and tap on it 7-10 times. This will enable developer options. Navigate back to the setting menu, and open the developer options. From here you may enable USB debugging.
	- Verify this worked correctly by running `adb devices`. You should see your device listed as: `<deviceId> device`.
		- If it does not show anything then most likely have to install your device's USB drivers for linux.
		- If it shows `<deviceId> unauthorized` make sure to connect the phone and tap ok on the popup asking you for permission to allow usb debugging.

- Only tested on linux systems. May not work on Windows as it uses UNIX style OS calls.

- In order to test if your device is recognized, it is highly recommended that under developer options, the "show touches" and "show swipes" options are enabled.


## Quick Use Guide
- The idea is that you can use the CLI tool to explore what is possible, and then you can script things as can be seen in the example below.
- Run androidAutomateCli with `./androidAutomateCli` in the project root directory.
- If this does not work you may have to add permissions with `sudo cmod +x androidAutomateCli`
- Choose your device from the list.
- From here record touch events, play touch events, explore and search installed apps, aswell as discovered the names of clickable nodes.

#### How to Record Events:
- Choose "Record Event" in the CLI menu.
- Provide a name for the event i.e: "send_snapchat".
- Perform the action on the device.
- Press CTRL-C to stop recording.
- The event is now stored in ./events and can be viewed and edited. The format of storing touch events is up for review and may change.

#### How to Playback Events:
- Choose "Playback Event" in the CLI menu.
- The available events will be listed with numbers.
- Provide the number of the event.
- Make sure the device is in the same state as when you recorded the event.
- The event will now play.

#### Searching for an app:
- Choose "Search Application".
- Provide a search criteria term like you would with grep (Internaly it is just grep on the output of the list applications output).

#### List Clickable Nodes
- Choose "List Clickable Nodes" in the CLI menu.
- The info for all of the currently clickable nodes will be displayed.
- The "content-desc" string will be used for matching nodes to click on in the tapNode() function.
- If the node you would like to click is not listed, you can look in the generated screendump.xml file to look for issues.
- NOTE: parseScreenXML() matches only nodes that have the atribute clickable="true".

#### Tap Clickable Node
- Choose "Tap Clickable Node" in the CLI menu.
- Provide a keyword of sub-string (case-insensitive) of "Text" or "Content-desc" from the output of the "List Clickable Nodes" output. This will tap the first node matching such criteria.


## Writing Scripts
This module provides the option of importing the main androidAutomate.py file to programmatically control your automation task.
```python
# SAMPLE AUTOMATION SCRIPT
from androidAutomate import Device
import time

# Argument is determined from `adb devices` command. In this case it is a Samsung s5
myDevice = Device("0283548d344b7a24")

# Use the CLI to determine package names for launching
myDevice.launchApp("com.android.settings")

# Wait for app to load / **REPLACE WITH FUNCTION TO DETECT WHEN APP LOADS** /
time.sleep(2)

# Tap on the searchbar (the possible tappable things are found in the CLI option "list Clickable Nodes")
myDevice.tapNode("Search")

# input text to the search bar:
myDevice.inputText("TEST")

# swipe up a couple times
for i in range(4):      #x1   y1    x2   y2
    myDevice.inputSwipe(500, 1300, 500, 400) #This represents a swipe up
    time.sleep(0.2)

# Demonstrate swipe options
myDevice.inputSwipe(500, 800, 500, 400, 1000) #This represents a swipe up but slow
myDevice.inputSwipe(50, 80, 50, 20, percent=True) #This represents a swipe up but with the x and y inputs being a percentage
```
This is an example script where the deviceId is passed during the instanciation of the device. The deviceId can be determined from the command `adb devices`.
The eventId is a parameter that identifies the touchscreen hardware id. It is determined automatically by the funciton detEventId(). This function can fail under certain circumstances in which case you will need to run the command `adb shell getevent -lp` and find the eventId. This can then be used to overwrite the incorrect eventId determined in the instanciation of the device.


## API Reference
### The [API reference](https://github.com/KonradStanski/androidAutomate/wiki/1.-API-Reference) and [Source Code](https://github.com/KonradStanski/androidAutomate/wiki/3.-API-Source-Code) can be found on the GitHub Wiki!
### The Emulator Options can be found and referenced [HERE](https://developer.android.com/studio/run/emulator-commandline)


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
Set device.eventId to the eventId in /dev/input/event<eventId>. In this case it is 2. This can be achieved with: `myDevice.eventId = <deviceId>`

**2.**
	If your device is **not showing up** in the `adb devices` command, look here for more info:

	https://stackoverflow.com/questions/21170392/android-device-does-not-show-up-in-adb-list/21470729
	https://forums.oneplus.com/threads/device-not-listing-using-adb-on-ubuntu-14-04-3.418957/
	https://stackoverflow.com/questions/32151114/adb-is-not-detecting-my-android-device-on-ubuntu

**3.**
	If your device shows up as **<deviceId> unauthorized** there are a couple things to check:
		USB debugging in developer options is checked.
		Try running `adb kill-server` and then `adb start-server` after connecting your device. If you did not get a popup asking you if you trust usb debugging from this computer before, this should do it.

**4.**
	Currently replaying touchscreen touches is not supported on emulators. This is on the todo list. This issue arrizes from emulators not allowing executable files to be run over adb. Suggestions on workarounds appreciated.


### TODO
- [ ] add "waitOnApp()" functionality to wait for the activity to have the appname in it []
- [ ] add touchscreen playback cababilities to x86 architecture emulator devides. This can be done by compiling the source to x86 32 bit elf executable and by adding a system architecture identification routine to the contructor of device classes.
- [ ] add ability to click on specific id events []
- [ ] record and replay input from all /dev/input/event# numbers and hardware devices [] $Might be impossible?$
- [ ] add availability to go to sepcific tasks within an app []
- [ ] create monkeyrunner class as a full wrapper around the random aspect of the monkey runner library in python []
- [ ] add robust error catching and error messages []
- [ ] add clicking x'th matching node to the tapNode() funciton []
- [ ] add possibility or recording and going to certain key activities within an app
- [ ] add Emulator manager class for launchning avd's
- [ ] add Avd manager class for creating avd's

### DONE
- [X] update CLI to have "list clickable nodes of current activity"
- [X] convert cli to class based API
- [X] add a monkey runner function for random touch input
- [X] automatic event<#> detection
- [X] convert openApp to open a fresh copy of the app every time
- [X] proper object oriented class structure for API
- [X] add screen width dependent input events
- [X] make all cli inputs numbered


### CHANGELOG
V1.0:
	Basic funcionality is present
	can record, replay, chain, and script basic things.

V1.1:
	Converted to class based structure with python API
	Converted CLI to API
	Removed chains because they are redundant with scripts
	Screen Dependent Input events based on nodes
	Automatic event number detection
	MonkeyRunner Functionality added
	Screen width dependent input events


### For other Developers and Contributors:
**Please do not hesitate to contact me or raise issues! I am always glad to help**

This module is essentialy a wrapper around the adb shell providing all the niceties of pythonic automation.
The replay of events is done by pushing the event record file to the sd card of the phone, then pushing the compiled executable file located in the ./src/ folder to the phone
The event is then played back from within the phone. This is done as doing the touch playback using python to input adb commands is simply too slow and produces unusable amounts of lag.
Currently this recording method only records the output from one device, but i believe it is simple enough to convert it to record
all of the devices of the phone, including the hardware buttons. That is on the todo list.




# This is a device class for sending ADB commands to capture and replay touch input aswell as a variety of other android related actions
from subprocess import Popen, PIPE
import os
import time
import re




class Device():
# """
# This is the class that allows all the other funcitons to be called.
# Args:
# 	deviceID (str): The id of the device. Determined using `adb devices`
# """
	def __init__(self, deviceId):
		self.deviceId = deviceId
		self.eventId = self.detEventId()
		print(f"DEVICEID: {self.deviceId}")
		print(f"EVENTID: {self.eventId}")





	# INPUT METHODS ###################################################################################################
	def inputText(self, text):
		# """
		# Function that inputs text without opening a keyboard on the phone
		# Args:
		# 	text (str): Text to input
		# """
		os.system(f"adb -s {self.deviceId} shell input text '{text}'")

	def inputTap(self, x, y):
		# """
		# Function that inputs a tap at the (x,y) coordinates provided.
		# These can be viewed by turning on the taps and swipes option in developer options
		# Args:
		# 	x (int): x coordinate
		# 	y (int): y coordinate
		# """
		os.system(f"adb -s {self.deviceId} shell input tap {x} {y}")

	def inputSwipe(self, x1, y1, x2, y2):
		# """
		# Function that inputs a swipe starting at (x1, y1) and going to (x2, y2)
		# Args:
		# 	x1 (int): x coordinate of beginning location of swipe
		# 	y1 (int): y coordinate of beginning location of swipe
		# 	x2 (int): x coordinate of end location of swipe
		# 	y2 (int): y coordinate of end location of swipe
		# """
		os.system(f"adb -s {self.deviceId} shell input swipe {x1} {y1} {x2} {y2}")

	def pressHome(self):
		# """
		# Function that pressed the center home button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_HOME")

	def pressBack(self):
		# """
		# Function that pressed the back button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_BACK")

	def pressPower(self):
		# """
		# Function that presses the power button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_POWER")

	def wakeup(self):
		# """
		# Function that presses the power button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_WAKEUP")

	def volumeUp(self):
		# """
		# Function that presses the volume up button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_UP")

	def volumeDown(self):
		# """
		# Function that presses the volume down button on your device
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_DOWN")

	def keycodeEvent(self, keycode):
		# """
		# Function that inputs a keycode to the device.
		# A reference list for keycodes can be found in the /keycodes.txt file
		# Args:
		# 	keycode (str/int): The string or integer description of the wanted keycode
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent {keycode}")

	def inputRandom(self, app, numEvents)
		# """
		# Function which uses the monkey runner module to open an app and input random events
		# Args:
		#	app (str): which app to launch for random input
		#	numEvents (int): number of random inputs to inject
		# """
		os.system(f"adb -s {self.deviceId} shell am force-stop {app}")
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v {numEvents}")


	# AUXILLIARY METHODS ############################################################################################
	def recordEvent(self, event):
		# """
		# function that records Touchscreen input until CTRL-C is typed into the terminal
		# Args:
		# 	event (str): Name of file to which the event will be saved.
		# """
		if not os.path.exists("events"): # make the events directory if it does not exist
			os.makedirs("events")
		os.system(f"adb -s {self.deviceId} shell getevent -t /dev/input/event{self.eventId} > ./events/{event}") # get input from device

	def playEvent(self, event):
		# """
		# Function that plays back a recorded event
		# Args:
		# 	event (str): Name of the recorded file to play
		# """
		os.system(f"adb -s {self.deviceId} push ./src/mysendevent /data/local/tmp/")
		os.system(f"adb -s {self.deviceId} push ./events/{event} /sdcard/")
		os.system(f"adb -s {self.deviceId} shell /data/local/tmp/mysendevent /dev/input/event{self.eventId} /sdcard/{event}")

	def launchApp(self, app):
		# """
		# Function that launches an app
		# Args:
		# 	app (str): Launches the supplied app. Apps may be listed in the CLI with listApps()
		# """
		os.system(f"adb -s {self.deviceId} shell am force-stop {app}")
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v 1")

	def listEvents(self):
		# """
		# Function that lists the contents of the /events/ folder
		# """
		# if events folder does not exist, make events folder
		if not os.path.exists("events"):
			os.makedirs("events")
		events = os.listdir("events") # fetch the contents of the folder
		if len(events) == 0: # if empty
			print("[EMPTY]")
		else: # print contents
			print("EVENTS:")
			for i in range(len(events)):
				print(f"[{i}]: {events[i]}")

	def searchApp(self, search):
		# """
		# Function that allows you to search your device for an app. Returns the name of the app
		# Args:
		# 	search (str): A search criteria that will grep through the output of the command `adb shell pm list packages`
		# """
		os.system(f"adb -s {self.deviceId} shell pm list packages | grep {search} -i")

	def listApps(self):
		# """
		# Function that will list all of the installed packages on your device
		# """
		os.system(f"adb -s {self.deviceId} shell pm list packages")

	def inputRandom(self, app, numEvents):
		# """
		# Function which uses the monkey runner module to open an app and input random events
		# Args:
		#	app (str): which app to launch for random input
		#	numEvents (int): number of random inputs to inject
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v {numEvents}")

	def detEventId(self):
		#"""
		# Function that self determines the eventId of the touch screen of the device.
		# IMPORTANT NOTE: eventId is determined by the first device that has the name "touch" in it.
		# It can be set manualy with myDevice.eventId = <eventId>
		#"""
		# Get output of adb shell getevent -lp command for parsing
		process = Popen(['adb','-s', self.deviceId,'shell', 'getevent', '-lp'], stdout=PIPE, stderr=PIPE)
		stdout, stderr = process.communicate()
		lines = stdout.decode().splitlines()
		# Process the output to determine the touch device event id
		for line in lines:
			if line[0:10] == "add device": # Match add device lines
				eventId = re.findall('(\d+)$', line)[0] # regex for getting the number at th end
			if line[0:7] == "  name:":
				if re.search("touch", line, re.IGNORECASE):
					print(f"Found eventId: {eventId}")
					return eventId
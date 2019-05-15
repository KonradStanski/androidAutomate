# This is a device class for sending ADB commands to capture and replay touch input aswell as a variety of other android related actions
from subprocess import Popen, PIPE
import os
import time




class Device():
"""
This is the class that allows all the other funcitons to be called.

Args:
	deviceID (str): The id of the device. Determined using `adb devices`
"""
	def __init__(self, deviceId):
		self.deviceId = deviceId
		self.eventId = 2#self.detEventId()
		print(f"EVENTID = {self.eventId}")


	def detEventId(self):
		pass


	def recordEvent(self, event):
		"""
		function that records Touchscreen input until CTRL-C is typed into the terminal

		Args:
			event (str): Name of file to which the event will be saved.
		"""
		if not os.path.exists("events"): # make the events directory if it does not exist
			os.makedirs("events")
		os.system(f"adb -s {self.deviceId} shell getevent -t /dev/input/event{self.eventId} > ./events/{event}") # get input from device


	def playEvent(self, event):
		"""
		Function that plays back a recorded event

		Args:
			event (str): Name of the recorded file to play
		"""
		os.system(f"adb -s {self.deviceId} push ./src/mysendevent /data/local/tmp/")
		os.system(f"adb -s {self.deviceId} push ./events/{event} /sdcard/")
		os.system(f"adb -s {self.deviceId} shell /data/local/tmp/mysendevent /dev/input/event{self.eventId} /sdcard/{event}")


	def playChain(self, chain):
		"""
		Function that plays a chain of events created in the CLI or manualy by editing a chain file

		Args:
			chain (str): Name of the chain to play
		"""
		file = open(f"./chains/{chain}", "r")
		for event in file:
			print(f"### CURRENTLY DOING ###: {event}")
			eval(event)
		file.close()


	def launchApp(self, app):
		"""
		Function that launches an app

		Args:
			app (str): Launches the supplied app. Apps may be listed in the CLI with listApps()
		"""
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v 1")


	def inputText(self, text):
		"""
		Function that inputs text without opening a keyboard on the phone

		Args:
			text (str): Text to input
		"""
		os.system(f"adb -s {self.deviceId} shell input text '{text}'")


	def inputTap(self, x, y):
		"""
		Function that inputs a tap at the (x,y) coordinates provided. These can be viewed by turning on
		the taps and swipes option in developer options

		Args:
			x (int): x coordinate
			y (int): y coordinate
		"""
		os.system(f"adb -s {self.deviceId} shell input tap {x} {y}")


	def inputSwipe(self, x1, y1, x2, y2):
		"""
		Function that inputs a swipe starting at (x1, y1) and going to (x2, y2)

		Args:
			x1 (int): x coordinate of beginning location of swipe
			y1 (int): y coordinate of beginning location of swipe
			x2 (int): x coordinate of end location of swipe
			y2 (int): y coordinate of end location of swipe
		"""
		os.system(f"adb -s {self.deviceId} shell input swipe {x1} {y1} {x2} {y2}")


	def pressHome(self):
		"""
		Function that pressed the center home button on your device
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_HOME")


	def pressBack(self):
		"""
		Function that pressed the back button on your device
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_BACK")


	def pressPower(self):
		"""
		Function that presses the power button on your device
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_POWER")


	def volumeUp(self):
		"""
		Function that presses the volume up button on your device
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_UP")


	def volumeDown(self):
		"""
		Function that presses the volume down button on your device
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_DOWN")


	def keycodeEvent(self, keycode):
		"""
		Function that inputs a keycode to the device. A reference list for keycodes can be found in the /keycodes.txt file

		Args:
			keycode (str/int): The string or integer description of the wanted keycode
		"""
		os.system(f"adb -s {self.deviceId} shell input keyevent {keycode}")


	# Auxilliary Functions
	def listChains(self):
		"""
		Function that lists to stdout the contents of the /chains/ folder
		"""
		if not os.path.exists("chains"):
			os.makedirs("chains")
		chains = os.listdir("chains") # fetch the contents of the folder
		if len(chains) == 0: # if empty
			print("[EMPTY]")
		else: # print contents
			print("CHAINS:")
			for i in range(len(chains)):
				print(f"[{i}]: {chains[i]}")


	def listEvents(self):
		"""
		Function that lists the contents of the /events/ folder
		"""
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
		"""
		Function that allows you to search your device for an app. Returns the name of the app

		Args:
			search (str): A search criteria that will grep through the output of the command `adb shell pm list packages`
		"""
		os.system(f"adb -s {self.deviceId} shell pm list packages | grep {search} -i")


	def listApps(self):
		"""
		Function that will list all of the installed packages on your device
		"""
		os.system(f"adb -s {self.deviceId} shell pm list packages")














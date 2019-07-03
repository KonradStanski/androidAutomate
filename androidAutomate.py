# This is a device class for sending ADB commands to capture and replay touch input aswell as a variety of other android related actions
from subprocess import Popen, PIPE
import os
import time
import re
import math


def retSysCall(command):
	# Simple function that returns the output from a system call
	process = Popen(command.split(), stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	lines = stdout.decode().splitlines()
	return lines

########################################################################################################################
###############################################Device Class#############################################################
########################################################################################################################
class Device:
# """
# This is the class that provides the device automation API
# Args:
# 	deviceID (str): The id of the device. Determined using `adb devices`
# 	verbose (bool): true by default, decides if instanciation info is printed
# """
	def __init__(self, deviceId=False, verbose=True):
		if not deviceId:
			print("No deviceId Specified! Here are some available devices:")
			os.system("adb devices")
			quit()
		self.verbose = verbose
		# check if deviceId valid
		self.deviceId = self.validateDevice(deviceId)
		if self.deviceId == False: # validateDevice returns False if the deviceId provided is not in `adb devices`
			print("Invalid deviceId")
			quit()
		self.eventId = self.detEventId()
		self.screenWidth, self.screenHeight = self.screenSize()
		if self.verbose:
			print(f"Valid deviceId: {self.deviceId}")
			print(f"Screen Width: {self.screenWidth}")
			print(f"Screen Height: {self.screenHeight}\n")


	# INPUT METHODS ###################################################################################################
	def inputTap(self, x, y, percent=False):
		# """
		# Function that inputs a tap at the (x,y) coordinates provided.
		# These can be viewed by turning on the taps and swipes option in developer options
		# Args:
		# 	x (int): x coordinate
		# 	y (int): y coordinate
		# Optional Args:
		# 	percent="True" (False by default): Sets the x,y input mode to percent of screen size
		# """
		if percent:
			x = (x/100)*self.screenWidth
			y = (y/100)*self.screenHeight
			os.system(f"adb -s {self.deviceId} shell input tap {x} {y}")
		else:
			os.system(f"adb -s {self.deviceId} shell input tap {x} {y}")

	def inputSwipe(self, x1, y1, x2, y2, time=200, percent=False):
		# """
		# Function that inputs a swipe starting at (x1, y1) and going to (x2, y2)
		# Args:
		# 	x1 (int): x coordinate of beginning location of swipe
		# 	y1 (int): y coordinate of beginning location of swipe
		# 	x2 (int): x coordinate of end location of swipe
		# 	y2 (int): y coordinate of end location of swipe
		# Optional Args:
		# 	time (int): the time (ms) to perform swipe. Default: 200ms
		# 	percent="True" (False by default): Sets the x, y input mode to percent of screen size
		# """
		if percent:
			x1 = (x1/100)*self.screenWidth
			y1 = (y1/100)*self.screenHeight
			x2 = (x2/100)*self.screenWidth
			y2 = (y2/100)*self.screenHeight
			os.system(f"adb -s {self.deviceId} shell input swipe {x1} {y1} {x2} {y2} {time}")
		else:
			os.system(f"adb -s {self.deviceId} shell input swipe {x1} {y1} {x2} {y2} {time}")

	def inputText(self, text):
		# """
		# Function that inputs text without opening a keyboard on the phone
		# Args:
		# 	text (str): Text to input
		# """
		os.system(f"adb -s {self.deviceId} shell input text '{text}'")

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
		# Function that wake's your device if it is not already awake
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_WAKEUP")

	def sleep(self):
		# """
		# Function that puts your device to sleep if it is awake
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_SLEEP")

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
		# A reference list for keycodes can be found in the Github Wiki
		# Args:
		# 	keycode (str/int): The string or integer description of the wanted keycode
		# """
		os.system(f"adb -s {self.deviceId} shell input keyevent {keycode}")

	def inputRandom(self, app, numEvents):
		# """
		# Function which uses the monkey runner module to open an app and input random events
		# Args:
		#	app (str): which app to launch for random input
		#	numEvents (int): number of random inputs to inject
		# """
		os.system(f"adb -s {self.deviceId} shell am force-stop {app}")
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v {numEvents}")

	def tapNode(self, nodeName):
		# """
		# Function that inputs a tap on the item described by its content-desc
		# Args:
		# 	nodeName (str): the content-desc of the node or the text
		nodes = self.parseScreenXML()
		nodeName = nodeName.lower()
		for item in nodes:
			if (nodeName in item.content_desc.lower()) or (nodeName in item.text_content.lower()):
				self.inputTap(item.center[0], item.center[1])
				break


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
		os.system(f"adb -s {self.deviceId} push ./src/mysendevent_arm /data/local/tmp/")
		os.system(f"adb -s {self.deviceId} push ./events/{event} /sdcard/")
		os.system(f"adb -s {self.deviceId} shell /data/local/tmp/mysendevent_arm /dev/input/event{self.eventId} /sdcard/{event}")

	def launchApp(self, app):
		# """
		# Function that launches an app
		# Args:
		# 	app (str): Launches the supplied app. Apps may be listed in the CLI with listApps()
		# """
		os.system(f"adb -s {self.deviceId} shell am force-stop {app}")
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v 1")
		# wait for app to open
		# line = [""]
		# while app not in line[0]:
		# 	process = Popen(['adb','-s', self.deviceId,'shell', ' dumpsys', 'window', 'windows', '|', 'grep', '-E', '"mFocusedApp"'], stdout=PIPE, stderr=PIPE)
		# 	stdout, stderr = process.communicate()
		# 	line = stdout.decode().splitlines()
		# time.sleep(1) #wait for the intended view to show up

	def closeApp(self, app):
		# """
		# Function that closes an app
		# Args:
		# 	app (str): Closes the supplied app. Apps may be listed in the CLI with listApps()
		# """
		os.system(f"adb -s {self.deviceId} shell am force-stop {app}")

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
			return events

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

	def detEventId(self):
		# """
		# Function that self determines the eventId of the touch screen of the device.
		# IMPORTANT NOTE: eventId is determined by the first device that has the name "touch" in it.
		# It can be set manualy with myDevice.eventId = <eventId>
		# returns:
		# 	eventId (str): the number corresponding to the touch screen eventId
		# """
		# Get output of adb shell getevent -lp command for parsing
		lines = retSysCall(f"adb -s {self.deviceId} shell getevent -lp")
		# Process the output to determine the touch device event id
		for line in lines:
			if line[0:10] == "add device": # Match add device lines
				# print(line[0:10])
				eventId = re.findall('(\d+)$', line)[0] # regex for getting the number at the end
			if line[0:7] == "  name:":
				if re.search("touch", line, re.IGNORECASE) or re.search("qwerty", line, re.IGNORECASE):
					if self.verbose:
						print(f"Found eventId: '{eventId}' in: '{line}'")
					return eventId
		# Nothing was found
		return "###EventId-not-found###"

	def screenSize(self):
		#"""
		# Function that self determines the screen size of the device.
		# returns:
		# 	width (int): the width of the device in pixels
		# 	height (int): the height of the device in pixels
		#"""
		# Get output for parsing
		lines = retSysCall(f"adb -s {self.deviceId} shell wm size")
		# Determine size
		for line in lines:
			width, height = (line.split(" ")[2]).split("x")
		return int(width), int(height)

	def parseScreenXML(self):
		# """
		# Function to parse the current view for clickable nodes
		# Returns:
		# 	nodes (list of node objects): a list of node objects for further processing
		# """
		# Get screen dump to file
		os.system(f"adb -s {self.deviceId} pull $(adb -s {self.deviceId} shell uiautomator dump | grep -oP '[^ ]+.xml') ./screendump.xml")
		# Process xml and output it to file for viewing pleasure
		file = open("screendump.xml", "r+")
		dumpfile = file.read()
		dump = dumpfile
		dumpfile = dumpfile.replace("><", ">\n<")
		file.close()
		file = open("screendump.xml", "w+")
		file.write(dumpfile)
		file.close()
		# determine clickable nodes
		remove = []
		dump  = dump.split("><")
		# remove invalid nodes
		for i in range(len(dump)):
			if 'index' not in dump[i]:
				dump[i] = ""
			if ('text=""' in dump[i]) and ('content-desc=""' in dump[i]):
				dump[i] = ""
		# Process the xml to identify clickable nodes
		dump = list(filter(None, dump))
		class node():
			def __init__(self, text):
				self.text_content = re.findall(r'text="(.*?)"', text)
				if self.text_content: # fixes weird empty field error
					self.text_content = self.text_content[0]
				self.resource_id = re.findall(r'resource-id="(.*?)"', text)[0]
				self.class_id = re.findall(r'class="(.*?)"', text)[0]
				self.package_id = re.findall(r'package="(.*?)"', text)[0]
				self.content_desc = re.findall(r'content-desc="(.*?)"', text)[0]
				# Determine the bounds
				self.bounds = re.findall(r'bounds="(.*?)"', text)[0]
				self.bounds = [int(x) for x in re.findall(r'[\d]+',self.bounds)]
				# This line just does the math to determine the xy from the bounds
				self.center = [math.floor(self.bounds[0]+((self.bounds[2]-self.bounds[0])/2)), math.floor(self.bounds[1]+((self.bounds[3]-self.bounds[1])/2))]
		# Create List of node objects
		nodes = []
		for text in dump:
			nodes.append(node(text))
		return nodes # return nodes if required for further processing

	def validateDevice(self, deviceId):
		# """
		# Function that validates a deviceId
		# Args:
		# 	deviceId (int): the deviceId to validate
		# Returns:
		# 	deviceId or False: depending on the outcome of validation
		# """
		lines = retSysCall(f"adb devices")
		# Determine size
		for line in lines[1:]:
			if deviceId in line:
				return deviceId
		return False


########################################################################################################################
###############################################Emulator Class###########################################################
########################################################################################################################
class Emulator:
# """
# This allows for the mangment of emulator devices
# Args:
# 	emulatorId (str): the name of the emulator to launch
# """
	def __init__(self, emulatorId=False, verbose=True):
		self.verbose = verbose
		self.options = False
		if not emulatorId:
			if self.verbose:
				print("No Emulator Specified! Here are the available emulators:")
				os.system("emulator -list-avds")
		else:
			self.emulatorId = emulatorId
			self.options = []
			if self.verbose:
				print(f"EmulatorId: {self.emulatorId}")

	# BASIC EMULATOR MANAGMENT ####################################################################################
	def startEmulator(self):
		initDev = retSysCall("adb devices") # used for determining the deviceId
		cliString = f"emulator -avd {self.emulatorId}"
		if self.options:
			print(f"Options are: {self.options}")
			cliString += " " + ' '.join(self.options)
		if self.verbose:
			cliString += " > /dev/null"
		cliString += " &" # to detach the terminal so that python execution can continue
		if not self.verbose:
			print("\n" + cliString + "\n")
		os.system(cliString)
		# Determine the device id of the emulator by comparing before and after lists of devices attached to system
		time.sleep(2)
		afterDev = retSysCall("adb devices")
		self.deviceId = (set(afterDev)-set(initDev)).pop().split()[0]
		print(self.deviceId)

	def stopEmulator(self):
		os.system(f"adb -s {self.deviceId} emu kill")

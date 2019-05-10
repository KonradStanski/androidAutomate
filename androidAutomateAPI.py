# This is a terminal emulator for capturing and replaying android things
from subprocess import Popen, PIPE
import os
import time

global eventId
eventId = 2

global deviceId
deviceId = "384852514b573398"

# START device CLASS definition ########################################




















# END device CLASS definition ##########################################




# used to determine the event number from the command
# adb shell getevent -lp. Need to identify the touch device
def detEventId():
	pass


# ACTION DEFINITIONS FOR API ######################################################
def recordEvent(event):
	# make the events directory if it does not exist
	if not os.path.exists("events"):
		os.makedirs("events")
	# get input from device
	os.system(f"adb -s {deviceId} shell getevent -t /dev/input/event{eventId} > ./events/{event}")


def playEvent(event):
	os.system(f"adb -s {deviceId} push ./src/mysendevent /data/local/tmp/")
	os.system(f"adb -s {deviceId} push ./events/{event} /sdcard/")
	os.system(f"adb -s {deviceId} shell /data/local/tmp/mysendevent /dev/input/event{eventId} /sdcard/{event}")


def playChain(chain):
	file = open(f"./chains/{chain}", "r")
	for event in file:
		print(f"### CURRENTLY DOING ###: {event}")
		eval(event)
	file.close()


def launchApp(app):
	os.system(f"adb -s {deviceId} shell monkey -p {app} -v 1")


def inputText(text):
	os.system(f"adb -s {deviceId} shell input text '{text}'")


def inputTap(x, y):
	os.system(f"adb -s {deviceId} shell input tap {x} {y}")


def inputSwipe(x1, y1, x2, y2):
	os.system(f"adb -s {deviceId} shell input swipe {x1} {y1} {x2} {y2}")


def pressHome():
	os.system(f"adb -s {deviceId} shell input keyevent KEYCODE_HOME")


def pressBack():
	os.system(f"adb -s {deviceId} shell input keyevent KEYCODE_BACK")


def pressPower():
	os.system(f"adb -s {deviceId} shell input keyevent KEYCODE_POWER")


def volumeUp():
	os.system(f"adb -s {deviceId} shell input keyevent KEYCODE_VOLUME_UP")


def volumeDown():
	os.system(f"adb -s {deviceId} shell input keyevent KEYCODE_VOLUME_DOWN")


def keycodeEvent(keycode):
	os.system(f"adb -s {deviceId} shell input keyevent {keycode}")



# LIST FUNCTIONS #############################################################
def listChains():
	if not os.path.exists("chains"):
		os.makedirs("chains")
	chains = os.listdir("chains") # fetch the contents of the folder
	if len(chains) == 0: # if empty
		print("[EMPTY]")
	else: # print contents
		print("CHAINS:")
		for i in range(len(chains)):
			print(f"[{i}]: {chains[i]}")


def listEvents():
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


# MENU CONTROL ################################################################
def deviceSelect():
	clear()
	printHead()
	print("Please Choose A Device:")
	process = Popen(['adb', 'devices'], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	lines = stdout.decode().splitlines()
	if len(lines) == 1:
		print("No devices found!")
	else:
		for i in range(1, len(lines)-1): # print devices
			print(f"[{i-1}]: {lines[i]}")
		deviceNum = input("Device #: ") # get user input for selection
		if deviceNum == "":
			deviceSelect()
		elif not deviceNum.isdigit():
			input("[PLEASE INPUT VALID ENTRY]")
			deviceSelect()
		elif int(deviceNum) >= len(lines)-1:
			input("[PLEASE INPUT VALID ENTRY]")
			deviceSelect()
		else:
			deviceNum = int(deviceNum)
			global deviceId
			deviceId = lines[deviceNum + 1].split("\t")[0] # get ID
			clear()






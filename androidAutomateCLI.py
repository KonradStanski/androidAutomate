# This is a terminal emulator for capturing and replaying android things
from subprocess import Popen, PIPE
import os
import time
import math
from androidAutomateAPI import Device


## Will be redundant after detEventId() method is implemented ###
global eventId
eventId = 2
#################################################################


# standard header
def printHead():
	# print("##################################################")
	# print("#                                                #")
	# print("#             androidAutomate V 1.1              #")
	# print("#                                                #")
	# print("##################################################")
	width = int(os.popen('stty size', 'r').read().split()[1])
	line = "#"*int(width)
	space = "#" + " "*(width-2) + "#"
	name = "#" + " "*math.floor(((width - 22)/2)) + "androidAutomate V 1.1" + " "*math.floor(((width - 22)/2)) + "#"
	print(  f"{line}\n"
			f"{space}\n"
			f"{name}\n"
			f"{space}\n"
			f"{line}")

# used to clear the screen
def clear():
	os.system("clear -x")

# used to quit the terminal app
def exitMenu():
	clear()
	quit()


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
			# global deviceId
			deviceId = lines[deviceNum + 1].split("\t")[0] # get ID
			clear()
			return deviceId


def actionSelect():
	# These are the available menu options
	actions = ["recordEventOp()", "playEventOp()",
				"listAppsOp()", "searchAppOp()", "exitMenu()"]
	clear()
	printHead()
	# get width of screen for dividing line
	width = int(os.popen('stty size', 'r').read().split()[1])
	line = "#"*width
	print(  f"[0]: Record Event\n"
			f"[1]: Playback Event\n"
			f"[2]: List Applications\n"
			f"[3]: Search Application\n"
			f"[4]: Exit\n"
			f"{line}")
	# take input and validate it
	actionNum = input("Action #: ")
	if actionNum == "":
		actionSelect()
	elif not actionNum.isdigit():
		input("[PLEASE INPUT VALID ENTRY]")
		actionSelect()
	elif int(actionNum) >= len(actions):
		input("[PLEASE INPUT VALID ENTRY]")
		actionSelect()
	else:
		# If valid, call the function at the corresponding index
		actionNum = int(actionNum)
		eval(actions[actionNum])


# MENU DEFINITIONS ##############################################################
# records the actions
def recordEventOp():
	clear()
	printHead()
	event = input("Please provide a filename to start recording: ")
	print("Press CTRL+C to end recording")
	myDevice.recordEvent(event)
	input("[PRESS ENTER]")
	actionSelect()

# plays a recorded event
def playEventOp():
	clear()
	printHead()
	myDevice.listEvents()
	event = input("Filename of event to play: ")
	print(f"playing {event} to {myDevice.deviceId}")
	myDevice.playEvent(event)
	input("[PRESS ENTER]")
	actionSelect()

# Prints a list of all installed apps
def listAppsOp():
	clear()
	printHead()
	print(f"Listing Apps on {myDevice.deviceId} ...")
	myDevice.listApps()
	input("[PRESS ENTER]")
	actionSelect()

# allows user to search for app
def searchAppOp():
	clear()
	printHead()
	search = input("Please provide a search criteria: ")
	myDevice.searchApp(search)
	input("[PRESS ENTER]")
	actionSelect()

# launches the provided app
def launchAppOp():
	clear()
	printHead()
	app = input("Please type full app name <ex: com.whatsapp>: ")
	myDevice.launchApp(app)
	input("[PRESS ENTER]")
	actionSelect()


# MAIN FUNCTION ####################################################################
def main():
	clear()
	deviceId = deviceSelect()
	global myDevice
	myDevice = Device(deviceId)
	actionSelect()


# play if launched from terminal
if __name__ == '__main__':
	main()
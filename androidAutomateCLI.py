# This is a terminal emulator for capturing and replaying android things
from subprocess import Popen, PIPE
import os
import time
from androidAutomateAPI import Device

global eventId
eventId = 2

# standard header
def printHead():
	print("##################################################")
	print("#                                                #")
	print("#             androidAutomate V 1.0              #")
	print("#                                                #")
	print("##################################################")


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
	actions = ["recordEventOp()", "playEventOp()",
				"listAppsOp()", "searchAppOp()", "exitMenu()"]
	clear()
	printHead()
	print("[0]: Record Event")
	print("[1]: Playback Event")
	print("###########################")
	print("[2]: List Applications")
	print("[3]: Search Application")
	print("###########################")
	print("[4]: Exit")
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
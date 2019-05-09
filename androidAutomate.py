# This is a terminal emulator for capturing and replaying android things
from subprocess import Popen, PIPE
import os
import time

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





def actionSelect():
	actions = ["recordEventOp()", "playEventOp()",
				 "createChainOp()", "playChainOp()", "listAppsOp()", "searchAppOp()",
				 "launchAppOp()", "exitMenu()"]
	clear()
	printHead()
	print("[0]: Record Event")
	print("[1]: Playback Event")
	print("###########################")
	print("[2]: Chain Events")
	print("[3]: Playback Chain")
	print("###########################")
	print("[4]: List Applications")
	print("[5]: Search Application")
	print("[6]: Launch Application")
	print("###########################")
	print("[7]: Exit")
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
	recordEvent(event)
	input("[PRESS ENTER]")
	actionSelect()


# plays a recorded event
def playEventOp():
	clear()
	printHead()
	listEvents()
	event = input("Filename of event to play: ")
	print(f"playing {event} to {deviceId}")
	playEvent(event)
	input("[PRESS ENTER]")
	actionSelect()



# create a chain
def createChainOp():
	clear()
	printHead()

	chain = input("Please provide filename for a new chain: ")
	if not os.path.exists("chains"):
		os.makedirs("chains")
	file = open(f"./chains/{chain}", "w+")

	writeFlag = True
	while writeFlag:
		clear()
		printHead()
		print("[0]: Add event")
		print("[1]: Add chain")
		print("[2]: Add delay")
		print("[3]: Add launch app")
		print("[4]: Add input text")
		print("[5]: Add tap")
		print("[6]: Add swipe")
		print("[7]: Finish")

		# take input and validate it
		actionNum = input("Action #: ")
		if actionNum == "":
			createChainOp()
		elif not actionNum.isdigit():
			input("[PLEASE INPUT VALID ENTRY]")
			createChainOp()
		elif int(actionNum) > 7:
			input("[PLEASE INPUT VALID ENTRY]")
			createChainOp()
		else:
			# If valid, call the function at the corresponding index
			actionNum = int(actionNum)
			if actionNum == 0: # event
				clear()
				printHead()
				listEvents()
				event = input("Please provide the filename of the event: ")
				file.write(f"playEvent('{event}')\n")
			if actionNum == 1: # chain
				clear()
				printHead()
				listChains()
				chain = input("Please provide the filename of the chain: ")
				file.write(f"playchain('{chain}')\n")
			if actionNum == 2: # delay
				clear()
				printHead()
				delay = input("Time (s) to delay: ")
				file.write(f"time.sleep({delay})\n")
			if actionNum == 3: # launch app
				clear()
				printHead()
				app = input("App to launch: ")
				file.write(f"launchApp('{app}')\n")
			if actionNum == 4: # input text
				clear()
				printHead()
				text = input("Text to input: ")
				file.write(f"inputText('{text}')\n")
			if actionNum == 5: # input tap
				clear()
				printHead()
				x, y = input("space seperated x y: ").split(" ")
				file.write(f"inputTap({x}, {y})\n")
			if actionNum == 6: # input swipe
				clear()
				printHead()
				x1, y1, x2, y2 = input("Space seperated x1 y1 x2 y2: ").split(" ")
				file.write(f"inputSwipe({x1}, {y1}, {x2}, {y2})\n")
			if actionNum == 7: # finish
				writeFlag = False
				file.close()
	actionSelect()


# play a chain
def playChainOp():
	clear()
	printHead()
	listChains()
	chain = input("Filename of chain to play: ")
	print(f"Playing {chain} to {deviceId}")
	playChain(chain)
	input("[PRESS ENTER]")
	actionSelect()


# Prints a list of all installed apps
def listAppsOp():
	clear()
	printHead()
	print(f"Listing Apps on {deviceId} ...")
	os.system(f"adb -s {deviceId} shell pm list packages")
	input("[PRESS ENTER]")
	actionSelect()


# allows user to search for app
def searchAppOp():
	clear()
	printHead()
	search = input("Please provide a search criteria: ")
	os.system(f"adb -s {deviceId} shell pm list packages | grep {search} -i")
	input("[PRESS ENTER]")
	actionSelect()


# launches the provided app
def launchAppOp():
	clear()
	printHead()
	app = input("Please type full app name <ex: com.whatsapp>: ")
	launchApp(app)
	input("[PRESS ENTER]")
	actionSelect()


# MAIN FUNCTION ####################################################################
def main():
	# os.system("sudo dnf install adb")
	clear()
	deviceSelect()
	actionSelect()


# play if launched from terminal
if __name__ == '__main__':
	main()
# This is a terminal emulator for capturing and replaying android things
from subprocess import Popen, PIPE
import os


def printHead():
	print("##################################################")
	print("#                                                #")
	print("#             androidAutomate V 1.0              #")
	print("#                                                #")
	print("##################################################")


def clear():
	os.system("clear -x")


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
			deviceId = lines[deviceNum + 1].split("\t")[0] # get ID
			clear()
			return deviceId


def actionSelect():
	actions = ["listEvents()", "recordEvent()", "playEvent()", "listChains()",
				 "chainEvents()", "playChains()", "listApps()", "launchApp()", "quit()"]
	clear()
	printHead()
	print("[0]: List Events")
	print("[1]: Record Event")
	print("[2]: Playback Event")
	print("[3]: List Chains")
	print("[4]: Chain Events")
	print("[5]: Playback Chain")
	print("[6]: List Applications")
	print("[7]: Launch Application")
	print("[8]: Quit")
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
		actionNum = int(actionNum)
		eval(actions[actionNum])



# ACTION DEFINITIONS ##############################################################
def listEvents():
	clear()
	printHead()
	print("Recorded Events:")
	# if events folder does not exist, make events folder
	if not os.path.exists("events"):
		os.makedirs("events")
	events = os.listdir("events") # fetch the contents of the folder
	if len(events) == 0: # if empty
		print("[EMPTY]")
	else: # print contents
		for i in range(len(events)):
			print(f"[{i}]: {events[i]}")
	input("[PRESS ENTER]")
	actionSelect() # return to main menu


# records the actions
def recordEvent():
	clear()
	printHead()
	fileName = input("Please provide a filename to start recording: ")
	print("Press CTRL+C to end recording")
	# make the events directory if it does not exist
	if not os.path.exists("events"):
		os.makedirs("events")
	# get input from device
	os.system(f"adb shell getevent -t /dev/input/event1 > ./events/{fileName}")
	input("[PRESS ENTER]")
	actionSelect()


def playEvent():
	clear()
	printHead()
	event = input("Please provide a filename to playback: ")
	print("playing")
	os.system("adb push ./src/mysendevent /data/local/tmp/")
	os.system(f"adb push ./events/{event} /sdcard/")
	os.system(f"adb shell /data/local/tmp/mysendevent /dev/input/event1 /sdcard/{event}")
	input("[PRESS ENTER]")
	actionSelect()


def listChains():
	clear()
	printHead()
	print("Created Chains: ")
	if not os.path.exists("chains"):
		os.makedirs("chains")
	chains = os.listdir("chains") # fetch the contents of the folder
	if len(chains) == 0: # if empty
		print("[EMPTY]")
	else: # print contents
		for i in range(len(chains)):
			print(f"[{i}]: {chains[i]}")
	input("[PRESS ENTER]")
	actionSelect()


def chainEvents():
	clear()
	printHead()
	print("test")
	input("[PRESS ENTER]")
	actionSelect()


def playChains():
	clear()
	printHead()
	print("test")
	input("[PRESS ENTER]")
	actionSelect()


# Prints a list of all installed apps
def listApps():
	clear()
	printHead()
	os.system("adb shell pm list packages")
	input("[PRESS ENTER]")
	actionSelect()


# launches the provided app
def launchApp():
	clear()
	printHead()
	app = input("Please type full app name <ex: com.whatsapp>: ")
	os.system(f"adb shell monkey -p {app} -v 1")
	input("[PRESS ENTER]")
	actionSelect()





# MAIN FUNCTION ####################################################################
def main():
	clear()
	deviceId = deviceSelect()
	actionSelect()


# play if launched from terminal
if __name__ == '__main__':
	main()
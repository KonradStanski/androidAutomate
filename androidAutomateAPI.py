# This is a device class for sending ADB commands to capture and replay touch input aswell as a variety of other android related actions
from subprocess import Popen, PIPE
import os
import time



"""
This module allows for the automation of

"""
class Device():
	def __init__(self, deviceId):
		self.deviceId = deviceId
		self.eventId = 2#self.detEventId()

	def detEventId(self):
		pass


	def recordEvent(self, event):
		# make the events directory if it does not exist
		if not os.path.exists("events"):
			os.makedirs("events")
		# get input from device
		os.system(f"adb -s {self.deviceId} shell getevent -t /dev/input/event{self.eventId} > ./events/{event}")


	def playEvent(self, event):
		os.system(f"adb -s {self.deviceId} push ./src/mysendevent /data/local/tmp/")
		os.system(f"adb -s {self.deviceId} push ./events/{event} /sdcard/")
		os.system(f"adb -s {self.deviceId} shell /data/local/tmp/mysendevent /dev/input/event{self.eventId} /sdcard/{event}")


	def playChain(self, chain):
		file = open(f"./chains/{chain}", "r")
		for event in file:
			print(f"### CURRENTLY DOING ###: {event}")
			eval(event)
		file.close()


	def launchApp(self, app):
		os.system(f"adb -s {self.deviceId} shell monkey -p {app} -v 1")


	def inputText(self, text):
		os.system(f"adb -s {self.deviceId} shell input text '{text}'")


	def inputTap(self, x, y):
		os.system(f"adb -s {self.deviceId} shell input tap {x} {y}")


	def inputSwipe(self, x1, y1, x2, y2):
		os.system(f"adb -s {self.deviceId} shell input swipe {x1} {y1} {x2} {y2}")


	def pressHome(self):
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_HOME")


	def pressBack(self):
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_BACK")


	def pressPower(self):
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_POWER")


	def volumeUp(self):
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_UP")


	def volumeDown(self):
		os.system(f"adb -s {self.deviceId} shell input keyevent KEYCODE_VOLUME_DOWN")


	def keycodeEvent(self, keycode):
		os.system(f"adb -s {self.deviceId} shell input keyevent {keycode}")


	# Auxilliary Functions
	def listChains(self):
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
		os.system(f"adb -s {self.deviceId} shell pm list packages | grep {search} -i")


	def listApps(self):
		os.system(f"adb -s {self.deviceId} shell pm list packages")














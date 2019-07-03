from androidAutomate import Emulator
import time

avd1 = Emulator("Pixel_2_API_Q")
avd1.options=["-tcpdump ~/code/androidAutomate/scripts/emu2.pcap", "-no-boot-anim", "-noaudio", "-port 5554"]
avd1.options.append("-no-snapshot-save")
avd1.startEmulator()

# avd2 = Emulator("Pixel_2_API_Q_2")
# avd2.options=["-tcpdump ~/code/androidAutomate/scripts/emu2.pcap", "-no-boot-anim", "-noaudio", "-port 5556"]
# avd2.options.append("-no-snapshot-save")
# avd2.startEmulator()

for i in range(10):
	time.sleep(1)
	print(i)


avd1.stopEmulator()
# avd2.stopEmulator()
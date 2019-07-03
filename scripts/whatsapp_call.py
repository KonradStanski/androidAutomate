# SAMPLE AUTOMATION SCRIPT
import sys
import os
sys.path.append(os.path.abspath("~/code/androidAutomate/androidAutomate.py"))
from androidAutomate import Device
import time
# Argument is determined from `adb devices` command. In this case it is a Samsung s9
# myDevice = Device("384852514b573398") #s9
emu1 = Device("emulator-5554") #eumlated pixel 2
emu2 = Device("emulator-5556") #eumlated pixel 2

# setup
emu1.wakeup()
emu2.wakeup()
emu1.launchApp("com.whatsapp")
emu2.launchApp("com.whatsapp")
time.sleep(3)

# Go to eachother
emu1.tapNode("Bsxsig2")
emu2.tapNode("Bsxsig1")

# Call
emu1.tapNode("Call")
time.sleep(3)
emu2.inputSwipe(550, 1600, 550, 900)

# Call for a bit
time.sleep(10)

# Emd call
emu1.inputTap(530, 1400)
emu2.inputTap(530, 1400)

# Close app
time.sleep(1)
emu1.closeApp("com.whatsapp")
emu2.closeApp("com.whatsapp")


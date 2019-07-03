# SAMPLE AUTOMATION SCRIPT
from androidAutomate import Device
import time

# myDevice = Device("384852514b573398") #s9
emu1 = Device("emulator-5554") #eumlated pixel 2
emu2 = Device("emulator-5556") #eumlated pixel 2

# setup
emu1.wakeup()
emu2.wakeup()
emu1.launchApp("com.instagram.android")
emu2.launchApp("com.instagram.android")
time.sleep(3)

# go to message
emu1.tapNode("message")
emu2.tapNode("message")

# go to eachother
emu1.tapNode("bsxsig")
emu2.tapNode("bsxsig")
time.sleep(1)

# Make the call
emu1.tapNode("Instagram Video Chat")
time.sleep(3)
emu2.inputTap(890, 128)

# Do a little talking
time.sleep(8)

# Close chat
emu1.tapNode("Close")
time.sleep(2)
emu1.tapNode("Poor")
emu2.tapNode("Poor")

# Close app
time.sleep(1)
emu1.closeApp("com.instagram.android")
emu2.closeApp("com.instagram.android")


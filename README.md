# androidAutomate
This repo provides a command line interface and API for recording and automating android tasks

# Utility Layout:
###Main Screen Options
[0]: List Events
[1]: Record Events
[2]: Playback Events
[3]: List Chains
[4]: Chain Events
[5]: Playback Chain
[6]: List Application
[7]: Launch Application
[8]: Exit



openApp = "adb shell monkey -p com.whatsapp -v 1"



record = "adb shell getevent -t /dev/input/event1 > recorded_touch_events.txt"

setup = "adb push mysendevent /data/local/tmp/"
sendToPhone = "adb push recorded_touch_events.txt /sdcard/"
playback = "adb shell /data/local/tmp/mysendevent /dev/input/event1 /sdcard/recorded_touch_events.txt"



adb -s emulator-5554 shell input swipe 1040 1422 125 1422
adb  shell pm list packages
adb shell getevent -l
adb -s 0283548d344b7a24 shell sendevent




adb shell getevent -t /dev/input/event1 > recorded_touch_events
adb push mysendevent /data/local/tmp/
adb push recorded_touch_events /sdcard/
adb shell /data/local/tmp/mysendevent /dev/input/event1 /sdcard/recorded_touch_events

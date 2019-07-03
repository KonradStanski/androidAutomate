#!/bin/bash


# Usefull
# https://developer.android.com/studio/run/emulator-commandline.html
# ~/Android/Sdk/emulator/emulator -accel-check
# ~/Android/Sdk/emulator/emulator -accel on
# -no-snapshot-save


# Launch Emulators 1 and 2
# Options: Force Hardware Acceleration, no boot animation, dont save after running and closing, no audio
~/Android/Sdk/emulator/emulator -avd Pixel_2_API_Q -tcpdump ~/code/androidAutomate/scripts/emu1.pcap -no-boot-anim -noaudio -port 5554 &
~/Android/Sdk/emulator/emulator -avd Pixel_2_API_Q_2 -tcpdump ~/code/androidAutomate/scripts/emu2.pcap -no-boot-anim -noaudio -port 5556 &


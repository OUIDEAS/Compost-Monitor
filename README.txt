COMPOST MONITOR README

Below are instructions and explanations for relevant scripts in this repo.







Connecting Sensors for Compost Monitor:
---------------------------------------
1. as dan@CompostMonitor, use ‘cd /sys/class/tty’ and ‘ls’
2. Take note of the ports listed
3. After each restart or any disconnection, unplug USB-A cable for the RedBoard. While holding down RESET on the RedBoard, plug the USB cable back in. 
4. Use ‘ls’ again. The RedBoard QWIIC shows up in /sys/class/tty as ‘ttyUSBX’, where X is an integer. It will default to the lowest integer that is unused (if ttyUSB0 and ttyUSB2 are already listed, the latest device to connect will be listed as ‘ttyUSB1’). 

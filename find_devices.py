#!/usr/bin/python

import subprocess
import os
import time
import signal
from database import *
import socket
import urllib2
import shutil

ifconfig = subprocess.check_output(["ifconfig"])

bestaande_interface=False;
interface=""
if "mon"in ifconfig:
	tempfile= open("ifconfig","wb")
	tempfile.write(ifconfig)
	tempfile.close()

	tempfile=open("ifconfig", "r")
	for line in tempfile:
		if "mon" in line:
			lineparts=line.split(" ")
			interface=lineparts[0]
	tempfile.close()
	os.remove("ifconfig")
else:
	os.system("sudo ifconfig wlan0 down")
	os.system("sudo airmon-ng start wlan0")
	interface="mon0"

os.makedirs ("/home/isis/dump")
command="sudo airodump-ng -w /home/isis/dump/dump "
command+=interface
print command
sub= subprocess.Popen(command,stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
time.sleep (60)
os.killpg(sub.pid, signal.SIGKILL)

lines= open ("dump/dump-01.csv")

clients=[]
process= False
for line in lines:
	if len (line)<3:
		process=False
	if process:
		lineparts= line.split(",")
		client={}
		client["MAC"]=lineparts[0]
		if lineparts[5] == " (not associated) ":
			client["associated_ap"]=''
		else:
			client["associated_ap"]=lineparts[5]
		networks= lineparts[6:]
		networks[-1]= networks[-1].rstrip()
		client ["networks"]=networks
		clients.append(client)
				
	if "Station MAC" in line:
		process= True


query= 'select location from units where caption="'
query+=socket.gethostname()
query+='";'
result=executequery (query)

location=result[0][0]
manufac_url = "http://api.macvendors.com/"

query= "insert into target_devices (MAC, location, timestamp, manufac, associated_ap) values\n "

for client in clients:
	query+="('"
	query+=client["MAC"]
	query+="','"
	query+=location
	query+="',now(),'"
	query+=urllib2.urlopen(manufac_url + client['MAC']).read()
	query+="','"
	query+=client["associated_ap"]
	query+="'),\n"

query=query[:-2]
query+=";"
print query
executequery(query)

shutil.rmtree("/home/isis/dump")
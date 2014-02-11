#! /usr/bin/python

import subprocess
import socket

from database import *

allinfo=subprocess.check_output(["sudo","iw", "wlan0", "scan", "passive"])

tempfile = open ("/tmp/ssid", "wb")
tempfile.write(allinfo)
tempfile.close()

list=[]
tempfile= open ("/tmp/ssid", "r")
for line in tempfile:
	if "SSID" in line:
		temp= (line.split(": "))
		ssid= (temp[1]);
		if (ssid.rstrip() not in list):
			list.append(ssid.rstrip())
tempfile.close()

for ssid in list:
	print (ssid)
	query= 'insert into wnets values ("'
	query+=ssid
	query+='","'
	query+=socket.gethostname()
	query+='",'
	query+="now()"
	query+=');'
	print (query)
	executequery(query)	

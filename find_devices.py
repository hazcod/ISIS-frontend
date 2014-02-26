#!/usr/bin/python

import subprocess
import os
import time
import signal
from database import *
import socket
import urllib2
import shutil
from monitor_management import *


def scan():
	interface=start_monitor("wlan0")

	os.makedirs ("/home/isis/dump")
	command="sudo airodump-ng -w /home/isis/dump/dump "
	command+=interface
	print command
	sub= subprocess.Popen(command,stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
	time.sleep (60)
	os.killpg(sub.pid, signal.SIGKILL)
	stop_monitor(interface)

def find_clients():
	lines= open ("/home/isis/dump/dump-01.csv")
	clients=[]
	process= False

	for line in lines:
		if len (line)<3:
			process=False
		
		if process:
			lineparts= line.split(",")
			client={}
			client["MAC"]=lineparts[0].lstrip();
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
	return clients

def post_clients(clients):
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
		try:
			query+=urllib2.urlopen(manufac_url + client['MAC']).read()
		except:
			query+="manufac website down"
		query+="','"
		query+=client["associated_ap"][1:]
		query+="'),\n"

	query=query[:-2]
	query+=";"
	print query
	executequery(query)

	query= "insert into probed_networks (MAC, SSID) values\n "
	for client in clients:
		query+="('"
		query+=client["MAC"]
		query+="','"
		for network in client["networks"]:
			query+=network
			query+="/"
		query+="'),\n"
	
	query=query[:-2]
	query+=";"
	executequery(query)
		

def cleanup():
	shutil.rmtree("/home/isis/dump")

if __name__ == '__main__':
	scan()
	clients= find_clients()
	post_clients(clients)
	cleanup()

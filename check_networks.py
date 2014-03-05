#! /usr/bin/python

import subprocess
import socket
import urllib2
import os

from database import *

manufac_url =  "http://api.macvendors.com/"

def main():
	scan()

def scan():
	allinfo= subprocess.check_output(["sudo", "iwlist", "wlan0","scan"])

	tempfile= open("/tmp/ssid","wb")
	tempfile.write(allinfo)
	tempfile.close()

	networks=[]
	network={}
	tempfile= open ("/tmp/ssid", "r")
	Error404=False
	for line in tempfile:
		if "Address" in line:
			lineparts= line.split(":", 1)
			MAC= lineparts[1].rstrip().lstrip()
			network={"MAC": MAC}
			networks.append(network)
			try:
				network['manufac'] = urllib2.urlopen(manufac_url + network['MAC']).read()
			except:
				Error404=True
				network['manufac']=""

		if "Channel:" in line:
			lineparts=line.split(":")
			channel= lineparts[1].rstrip()
			network["channel"]= channel
		if "Quality" in line:
			lineparts=line.split("=")
			lineparts2=lineparts[1].split("/")
			quality=lineparts2[0]
			network["quality"]=quality
		if "Encryption key" in line:
			lineparts=line.split(":")
			if lineparts[1].rstrip()=="off":
				network["enc"]="open"
		if "ESSID" in line:
			lineparts=line.split(":")
			SSID=lineparts[1].rstrip()
			network["SSID"]= SSID
		if "WPA" in line:
			lineparts= line.split("/")
			encPart=lineparts[-1].rstrip();
		if "Authentication Suites" in line:
			lineparts=line.split(":")
			encPart+=lineparts[1].rstrip()
			network["enc"]= encPart
		if "enc" not in network:
			network["enc"]= "WEP"


	query= "delete from ap_info where caption='"
	query+=socket.gethostname()
	query+="';"
	executequery(query)
	query="insert into ap_info(wifi_network,caption,quality,channel,mac_adress,encryption,manufac,last_updated) values "
	for network in networks:
		query+='('
		query+=network["SSID"]
		query+=',"'
		query+=socket.gethostname()
		query+='",'
		query+=network["quality"]
		query+=','
		query+=network["channel"]
		query+=',"'
		query+=network["MAC"]
		query+='","'
		query+=network["enc"]
		query+='","'
		query+=network['manufac']
		query+='",'
		query+="now()"
		query+="),\n"
	query=query[:-2]
	query+=";"
	executequery(query)
	os.remove ("/tmp/ssid")

	if Error404:
		raise Exception ("couldn't resolve manufacturer")

if __name__ == "__main__":
    main()
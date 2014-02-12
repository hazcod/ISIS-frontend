#! /usr/bin/python

import subprocess
import socket

from iwlistparse import *
from database import *

#lequery=''
raw=getNetworks()
for lijst in raw:
	#print(lijst)
	query='insert into ap_info(wifi_network,caption,quality,channel,mac_adress)  values ("';
	query+=lijst['Name']
	query+='","'
	query+=socket.gethostname()
	query+='","'
	query+=lijst['Quality'][:-2][-1:]
	query+='","'
	query+=lijst['Channel']
	query+='","'
	query+=lijst['Address']
	query+='"); '
	lequery+=query
	#print(query)
	executequery(query)
#executequery(lequery)
# for ssid in list:
# 	print (ssid)
# 	query= 'insert into wnets values ("'
# 	query+=ssid
# 	query+='","'
# 	query+=socket.gethostname()
# 	query+='",'
# 	query+="now()"
# 	query+=');'
# 	print (query)
# 	executequery(query)	

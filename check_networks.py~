#! /usr/bin/python

import subprocess
import socket

from iwlistparse import *
from database import *

raw=getNetworks()
for lijst in raw:
	query='insert into ap_info(wifi_network,caption,quality,channel,mac_adress, encryption)  values ("';
	query+=lijst['Name']
	query+='","'
	query+=socket.gethostname()
	query+='","'
	query+=lijst['Quality'][:-2][-1:]
	query+='","'
	query+=lijst['Channel']
	query+='","'
	query+=lijst['Address']
	query+='","'
	query+=lijst['Encryption']
	query+='"); '
	lequery+=query
	executequery(query)

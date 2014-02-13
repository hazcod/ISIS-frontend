#! /usr/bin/python

import subprocess
import socket

from iwlistparse import *
from database import *

raw=getNetworks()
if (len(raw) < 10):
	exit

removeq='delete from ap_info where (caption = "';
removeq+=socket.gethostname()
removeq+='");'
executequery(removeq)
for lijst in raw:
	query='insert into ap_info(wifi_network,caption,quality,channel,mac_adress,encryption, last_updated) values ("';
	query+=lijst['name']
	query+='","'
	query+=socket.gethostname()
	query+='","'
	query+=lijst['quality'][:-2][-1:]
	query+='","'
	query+=lijst['channel']
	query+='","'
	query+=lijst['address']
	query+='","'
	query+=lijst['encryption']
	query+='",now()); '
	executequery(query)

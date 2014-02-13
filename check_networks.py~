#! /usr/bin/python

import subprocess
import platform

from iwlistparse import *
from database import *

print('Starting getNetworks')
raw=getNetworks()
if (len(raw) < 2):
	die()
	print('Output < 10 lines, so dismissed.')
query=''
#dupreg = "\{'encryption': '.+', 'quality': '.+', 'name': '%s', 'channel': '.+', 'address': '%s'\}" % (lijst['name'], lijst['address'])
bigquery='insert into ap_info(wifi_network,caption,quality,channel,mac_adress,encryption, last_updated) values ';	
print(raw)	
for lijst in raw:
	dupreg = "\{'encryption': '.+', 'quality': '.+', 'name': '%s', 'channel': '.+', 'address': '%s'\}" % (lijst['name'], lijst['address'])
	print(dupreg)
	regex = re.compile(dupreg)
	r = regex.search(bigquery)
	if r==None:
		query+='("'
		query+=lijst['name']
		query+='","'
		query+=platform.node()
		query+='","'
		query+=lijst['quality'][:-2][-1:]
		query+='","'
		query+=lijst['channel']
		query+='","'
		query+=lijst['address']
		query+='","'
		query+=lijst['encryption']
		query+='",now()),'
		bigquery+=query
bigquery=bigquery[:-1]
bigquery+=';'
#print(bigquery)
removeq='delete from ap_info where (caption = "';
removeq+=platform.node()
removeq+='");'
executequery(removeq)
print('Cleared database prior to inserts.')
executequery(bigquery)

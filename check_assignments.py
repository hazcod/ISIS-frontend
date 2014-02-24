#!/usr/bin/python
import socket
import subprocess
import git
from database import *
from check_networks import *
from take_image import *
from kick_from_ap import *
from crack_network import *

def opdrachtvolbracht():
	query='update assignments SET status = "executed" where assignments_id ="'
	query+=str(ass_id[0][0])
	query+='";'
	executequery(query)
 
def opdrachterror(param):
	query='update assignments SET status = "error", parameter="'
	query+=param
	query+='" where assignments_id="'
	query+=str(ass_id[0][0])
	query+='";'
	executequery(query)

def opdrachtexecute():
	query='update assignments SET status = "busy" where assignments_id="'
	query+=str(ass_id[0][0])
	query+='";'
	executequery(query)

def getparameter():
	query='select parameter from assignments where caption="'
	query+=socket.gethostname()
	query+='" and status="new" order by 1 ASC limit 1;'
	kickpar= executequery(query)
	return kickpar

query='update units set last_seen = now() where caption="'
query+=socket.gethostname()
query+='";'

executequery(query)

query='select assignments_id from assignments where caption="'
query+=socket.gethostname()
query+='"and status="new" order by 1 ASC limit 1;'
ass_id= executequery(query)

query='select assignment from assignments where caption="'
query+=socket.gethostname()
query+='"and status="new" order by 1 ASC limit 1;'
assignments= executequery(query)

if assignments[0][0] == "gitCheckout":
	try:
		opdrachtexecute()
		repo = git.Repo('/home/isis/ISIS-frontend')
		o = repo.remotes.origin
		o.pull()
		opdrachtvolbracht()
	except AssertionError:
		opdrachtvolbracht()
	except:
		opdrachterror("Merge conflicts")

elif assignments[0][0]=="scan":
	try:
		opdrachtexecute()
		scan()
		opdrachtvolbracht()
	except subprocess.CalledProcessError:
		opdrachterror("Geen wifi-stick verbonden.")
	except Exception, e:
		opdrachterror(str (e))
elif assignments[0][0]=="snap":
	try:
		opdrachtexecute()
		take_picture()
		opdrachtvolbracht()
	except:
		opdrachterror("Geen camera verbonden.")
elif assignments[0][0]=="deauth":
	kickpar= getparameter()
	opdrachtexecute()
	print (kickpar)
	ap = kickpar[0][0].split('|')[0]
	target = kickpar[0][0].split('|')[1]
	channel = kickpar[0][0].split('|')[2]
	print ap
	print target
	print channel
	kick_ap(ap,channel,target)
	opdrachtvolbracht()
elif assignments[0][0]=="crackWifiUnit":
	try:
		ESSID=getparameter()[0][0]
		opdrachtexecute()
		crack_network(ESSID)
		opdrachtvolbracht()
	except Exception, e:
		opdrachterror(str(e))


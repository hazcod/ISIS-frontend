#!/usr/bin/python
import socket
import subprocess
import git
import re
from database import *
from check_networks import *

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
	opdrachtexecute()
	try:
		repo = git.Repo('/home/isis/ISIS-frontend')
		o = repo.remotes.origin
		o.pull()
		opdrachtvolbracht()
	except:
		opdrachterror("Git pull error")

elif assignments[0][0]=="scan":
	try:
		opdrachtexecute()
		scan()
		opdrachtvolbracht()
	except subprocess.CalledProcessError:
		opdrachterror("Geen wifi-stick verbonden.")
elif assignments[0][0]=="snap":
	try:
		opdrachtexecute()
		result = os.popen('sudo raspistill -o /home/isis/ISIS-frontend/image.jpg').read()
		if re.match('failed', result) is not None:
			sleep("5")
			os.system("scp  /home/isis/ISIS-frontend/image.jpg isis@192.168.255.54:/home/isis/Afbeeldingen/image.jpg")
			#subprocess.Popen("/home/isis/ISIS-frontend/take_image.sh",shell=True);
			opdrachtvolbracht()
		else:
			opdrachtErorr("Geen camera verbonden.")
	except:
		opdrachterror("Geen camera verbonden.")

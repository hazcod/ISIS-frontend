#!/usr/bin/python
import socket
import subprocess
from database import *

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
	subprocess.Popen("/home/isis/git/checkout_frontendGit",shell=True);
	query='update assignments SET status = "executed" where assignments_id ="'
	query+=str(ass_id[0][0])
	query+='";'
	executequery(query) 
#!/usr/bin/python
import socket
from database import *

query='update units set last_seen = now() where caption="'
query+=socket.gethostname()
query+='";'

executequery(query)

query='select * from assignments where caption="'
query+=socket.gethostname()
query+='";'
assignments= executequery(query)

for row in assignments:
	print (row)
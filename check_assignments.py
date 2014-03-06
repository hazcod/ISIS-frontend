#!/usr/bin/python

import socket
import subprocess
import git
import os.path
import check_networks

from database import *
from wifi import *
from take_image import *
from kick_from_ap import *
from crack_network import *
from rogue_ap import *
from find_devices import *

# File created when assignment is still running
file_busy = '/tmp/busy'

def opdrachtvolbracht():
	try:
		os.remove(file_busy)
	except:
		pass
	query = 'update assignments SET status = "executed" where assignments_id ="'
	query+= str(cmd_id)
	query+= '";'
	executequery(query)
 
def opdrachterror(errormsg):
	try:
		os.remove(file_busy)
	except:
		pass
	query = 'update assignments SET status = "error", parameter="'
	query+= errormsg
	query+= '" where assignments_id="'
	query+= str(cmd_id)
	query+= '";'
	print(query)
	executequery(query)

def opdrachtexecute():
	open(file_busy, 'a').close()
	query= 'update assignments SET status = "busy" where assignments_id="'
	query+= str(cmd_id)
	query+= '";'
	executequery(query)

def lastseen():
	# # Update last seen
	query='update units set last_seen = now() where caption="'
	query+=socket.gethostname()
	query+='";'
	executequery(query)

# Check into our hotel ..erm..website
lastseen()

# All your command are belong to us
query = "select assignment,assignments_id,parameter from assignments where caption='"
query+= socket.gethostname()
query+= "' and status='new' order by assignments_id ASC limit 1;"
tmp = executequery(query)
if tmp:
	command    = tmp[0][0]
	cmd_id     = tmp[0][1]
	parameter  = tmp[0][2]
else:
	print('No commands atm.')
	quit()

# Safe check for wipe, executed even when busy
if command == "wipe":
	try:
		#remove files gracefully
		print('ZOMG DELETE EVERYTHING')
	except:
		#force remove files
		print('WOW SUCH DELETE FORCE')
		
elif command == "stoprogue":
	try:
		opdrachtexecute()
		stop_rogue_ap()
		opdrachtvolbracht()
		opdrachtvolbracht()
		quit()
	except Exception, e:
		opdrachterror('Could not stop the rogue ' + str(e))

# Quit when there is an assignment still running
if os.path.isfile(file_busy):
	print('Still busy or no command	!')
	quit()

print('- Assignment check')
# Check for assignments
if command == "gitCheckout":
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
elif command == "scan":
	try:
		opdrachtexecute()
		check_networks.scan()
		opdrachtvolbracht()
	except subprocess.CalledProcessError:
		opdrachterror("Geen wifi-stick verbonden.")
	except Exception, e:
		opdrachterror('Scan error: ' + str (e))
elif command == "snap":
	try:
		opdrachtexecute()
		take_picture()
		opdrachtvolbracht()
	except:
		opdrachterror("Geen camera verbonden.")
elif command == "deauth":
	try:
		opdrachtexecute()
		ap = parameter.split('|')[0]
		target = parameter.split('|')[1]
		channel = parameter.split('|')[2]
		kick_ap(ap,channel,target)
		opdrachtvolbracht()
	except Exception, e:
		opdrachterror('Deauth failed: ' + str(e))	
elif command == "crackWifiUnit":
	try:
		opdrachtexecute()
		crack_network(parameter)
		opdrachtvolbracht()
	except Exception, e:
		opdrachterror('Crack failed: ' + str(e))
elif command == "rogue":
	try:
		opdrachtexecute()
		start_rogue_ap()
	except Exception, e:
		opdrachterror('Could not go rogue ' + str(e))
		
elif command == "finddevices":
	try:
		opdrachtexecute()
		find_devices()
		opdrachtvolbracht()
	except Exception, e:
		opdrachterror('Could not find devices ' + str(e))
elif command == "nmap":
        try:
                try:
	                opdrachtexecute()
			find_devices()
	                if "open" in parameter.split('|')[1]:
	                        connectWifiWEP(parameter.split('|')[0])
	                elif "wpa" in parameter.split('|')[1]:
	                        connectWifiWPA(parameter.split('|')[0],parameter.split('|')[2])
	                else:
	                        connectWifiWEP(parameter.split('|')[0],parameter.split('|')[2])
			map()
		finally:
			os.system('sudo cat "nameserver 8.8.8.8" > /etc/resolv.conf')
	except Exception, e:
		opdrachterror('NMAP PROBLEEM: ' + str(e))
else:
	opdrachterror('Unknown command ' + command)

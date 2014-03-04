#!/usr/bin/python

from server_settings import *

import os

print ("ssh sleutels zonder paswoord zijn vereist voor goede werking. Duw op enter als het paswoord wordt gevraagd.")
os.system("ssh-keygen")
os.system("sudo ssh-keygen")

command="ssh-copy-id "
command+=server_username
command+="@"
command+=server_address
os.system(command)
command= "sudo "+command
os.system(command)
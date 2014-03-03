#! /usr/bin/python

import subprocess
import socket
import re
import time
import os

from server_settings import *

def take_picture():
	result = subprocess.check_output(['sudo', 'raspistill', '-o' ,'/home/isis/ISIS-frontend/image.jpg'])
	if "failed" not in result:
		time.sleep(5)
		
		command="scp /home/isis/ISIS-frontend/image.jpg "
		command+=server_username
		command+="@"
		command+=server_address
		command+=":./Afbeeldingen/image.jpg"
		os.system("command")
	else:
		raise Exception("Camera is not found! (or some other error)")

if __name__=="__main__":
	take_picture()

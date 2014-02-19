#! /usr/bin/python

import subprocess
import socket
import re
import time
import os

def take_picture():
	result = subprocess.check_output(['sudo', 'raspistill', '-o' ,'/home/isis/ISIS-frontend/image.jpg'])
	if "failed" not in result:
		time.sleep(5)
		os.system("scp  /home/isis/ISIS-frontend/image.jpg isis@192.168.255.54:/home/isis/Afbeeldingen/image.jpg")
	else:
		raise Exception("Camera is not found! (or some other error)")

if __name__=="__main__":
	take_picture()

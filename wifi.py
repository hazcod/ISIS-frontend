#!/usr/bin/python

import os
import subprocess
import nmap
import socket
import re
import fcntl
from time import sleep
import struct
import netifaces as ni
from netaddr import IPNetwork
from database import *
from server_settings import *

nmap_results = list()
file_interf = '/etc/network/interfaces'
file_wpa = '/etc/wpa.conf'
wifi_c = "# WIFI"

def connectWifiWEP( ssid, passwd = False ):
	# Delete previous WIFI lines
	cleanupInterfaces()
	# Add new WIFI lines
	with open(file_interf, "a") as myfile:
		myfile.write(wifi_c + "\n auto wlan0\n")
		myfile.write(wifi_c + "\n iface wlan0 inet dhcp\n")
		myfile.write(wifi_c + "\n	wireless-essid " + ssid + "\n")
		if (passwd != False):
			myfile.write(wifi_c + "\n	wireless-key " + passwd + "\n")	
	os.system("sudo service networking restart")


def connectWifiWPA( ssid, passw ):
	os.system("sudo killall wpa*")
	os.system("sudo killall dhclient")
	os.system("sudo ifdown wlan0")
	# Delete previous WIFI lines
	cleanupInterfaces()

	output = subprocess.check_output(['wpa_passphrase',ssid,passw])
	f = open(file_wpa, "w")
	#print(output)
	f.write(str(output))
	f.close()
	subprocess.Popen(["wpa_supplicant", "-i", "wlan0", "-c", file_wpa])
	subprocess.Popen(["dhclient","-r"])
	subprocess.Popen(["dhclient","wlan0"])

def cleanupInterfaces():
	f = open(file_interf, "r")
	lines = f.readlines()
	f = open(file_interf, "w")
	d = 0
	for line in lines:
		if d == 0:
			if (wifi_c) in line:
				d = 1
		else:
			f.write(line)
	f.close()
	f.close()
	
def cleanupInterfaces_bckp():
	f = open(file_interf, "w")
	d = 0
	for line in lines:
		if d == 1:
			if "}" in line:
				d = 0
		else:
			if "ssid=" + ssid in line:
				d = 1
			else:
				f.write(line)

	f.close()	

def map(network = False):
	#ip_eth = ni.ifaddresses('eth0')[2][0]['addr']
	ip = ni.ifaddresses('wlan0')[2][0]['addr']
	print('ip: ' + ip)
	mask = socket.inet_ntoa(fcntl.ioctl(socket.socket(socket.AF_INET, socket.SOCK_DGRAM), 35099, struct.pack('256s', "wlan0"))[20:24]);
	print('mask: ' + mask)
	network_ip = str(IPNetwork(ip + '/' + mask).cidr);
	print('network ip: ' + network_ip)
	nm = nmap.PortScanner()
	print('Scanning..')
	r = nm.scan(hosts=network_ip, arguments='-T4 -A -v -e wlan0')
	for host in nm.all_hosts():
		if (nm[host].state() == 'up' and host != ip): #and host != ip_eth):
			print("Host up; " + host)
			query = "UPDATE target_devices SET info='"
			timestr = r['nmap']['scanstats']['timestr']
			query += timestr + '|'
			#print(timestr)
			#scaninfo = r['nmap']['scaninfo']
			for proto in nm[host].all_protocols():
				print("proto: " + proto)
				query+= proto + '/'
				for key in nm[host][proto].keys():
					query += str(key) + ','
					print('key: ' + str(key))
				query = query[:-1]
				query += ";"
			print("pinging")
			subprocess.Popen(["ping", "-c 1", host], stdout = subprocess.PIPE)
			print("arping")
			pid =subprocess.Popen(["arp", "-i","wlan0","-n", host], stdout = subprocess.PIPE)
			s = pid.communicate()[0]
			#sleep(1)
			print("ARP (raw): " + s)
			mac = re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", s)
			if (mac != None):
				mac = mac.groups()[0]
				query += "' WHERE mac='" + mac + "';"
				print(query)
				executequery(query)
			#print(scaninfo)
			#print(nm[host].all_protocols())
			#print(r['nmap'])
			#query += " WHERE (MAC = '" + r['scan'][nm[host].hostname()]['addresses']['mac'] + "')"

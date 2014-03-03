#!/usr/bin/python
import MySQLdb
from server_settings import *

def executequery (query):
	db = MySQLdb.connect(host=server_address, # your host, usually localhost
		user=database_user, # your username
		passwd=database_password, # your password
		db=database_name) # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the query you need
	cur = db.cursor()

	cur.execute(query)
	db.commit()
	return cur.fetchall()
#!/usr/bin/python
import MySQLdb

def executequery (query):
	db = MySQLdb.connect(host="193.191.187.44", # your host, usually localhost
		user="c7185zrc_isisU", # your username
		passwd="1wofRFQh", # your password
		db="c7185zrc_isis") # name of the data base

	# you must create a Cursor object. It will let
	#  you execute all the query you need
	cur = db.cursor()

	cur.execute(query)
	db.commit()
	return cur.fetchall()
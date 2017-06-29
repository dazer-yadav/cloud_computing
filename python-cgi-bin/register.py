#!/usr/bin/python2

import mysql.connector as mariadb  #import mariadb


import cgi
import cgitb

cgitb.enable()

print "content-type:text/html"

print ""

data=cgi.FormContent()		#taking form contents and saving each one in data

username=data['uname'][0]
password=data['upass'][0]
email_addr=data['email'][0]
contact=data['contact'][0]



x=mariadb.connect(user='root',password='redhat',database='lw')  #connecting to mariadb-server

y=x.cursor()

sql1="select username from users where username=%s"	#entering in database

y.execute(sql1,(username,))

result=y.fetchone()

trigger=str(result)		#if user already exist

if(trigger=='None'):
	sql="insert into users values(%s,%s,%s,%s);"
	y.execute(sql,(username,password,email_addr,contact))
	x.commit()
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/index.html\">\n")
else:
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/error.html\">\n")#or else send to errorpage
	






				








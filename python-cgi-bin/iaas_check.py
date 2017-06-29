#!/usr/bin/python2

import mysql.connector as mariadb
import cgi
import commands
import cgitb

cgitb.enable()

print "content-type:text/html"
print ""

data=cgi.FormContent()

username=data['uname'][0]

x=mariadb.connect(user='root',password='redhat',database='lw')

y=x.cursor()

sql="select user from iaas where user=%s"

y.execute(sql,(username,))

result=y.fetchone()

trigger=str(result)

if (trigger=='None'):
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/iaas_newuser.html\">\n"

else:
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/iaas_olduser.html\">\n"

x.close()
	

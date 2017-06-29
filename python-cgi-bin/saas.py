#!/usr/bin/python2

import cgi
import cgitb
import commands
import mysql.connector as mariadb

cgitb.enable()

print "content-type:text/html"

print ""

data=cgi.FormContent()

username=data['uname'][0]

password='object'


x=mariadb.connect(user='root',password='redhat',database='lw')

y=x.cursor()


sql="select user from common_users where user=%s;"


y.execute(sql,(username,))

result=y.fetchone()

trigger=str(result)

if(trigger=='None'):
	
	sql="insert into common_users values(%s);"
	y.execute(sql,(username,))
	x.commit()
	x.close()


	commands.getstatusoutput("sudo useradd {}".format(username))
	commands.getstatusoutput("sudo echo {} | sudo passwd {} --stdin ".format(password,username))
	commands.getstatusoutput("sudo systemctl restart sshd")
	commands.getstatusoutput("sudo setenforce 0")
	commands.getstatusoutput("sudo iptables -F")
	commands.getstatusoutput("sudo systemctl stop firewalld")
	


	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/saas_download.html\">\n")
	
else:

	commands.getstatusoutput(" sudo systemctl restart sshd")
	commands.getstatusoutput("sudo setenforce 0")
	commands.getstatusoutput("sudo iptables -F")
	commands.getstatusoutput("sudo systemctl stop firewalld")
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/saas_download.html\">\n")



	
	





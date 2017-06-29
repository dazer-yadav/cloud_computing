#!/usr/bin/python2

import mysql.connector as mariadb
import cgi
import commands
import cgitb

#this page is meant for old users to view their existing instances

cgitb.enable()

print "content-type:text/html"
print ""

data=cgi.FormContent()

username=data['uname'][0]

x=mariadb.connect(user='root',password='redhat',database='lw')

y=x.cursor()

sql="select port,web_port from iaas where user=%s" #selecting port for direct view...

y.execute(sql,(username,))

result=y.fetchall()

print result

for i in result:
	port=i[0]
	web_port=i[1]

print port
print web_port	
'''
x.close()


'''

#commands.getstatusoutput("sudo virsh start {} ".format(username))

status=commands.getstatusoutput("sudo /var/www/cgi-bin/websockify-master/run -D 192.168.43.112:{} 192.168.43.112:{}".format(web_port,port))


#if(status[0]==0):
print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/vnc/index.html?host=192.168.43.112&port={}\">\n".format(web_port))


#else:
#	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/iaas_olduser.html\">\n") '''





	
	


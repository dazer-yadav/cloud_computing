#!/usr/bin/python2

import mysql.connector as mariadb
import cgi
import commands
import cgitb
import random

cgitb.enable()

print "content-type:text/html"
print ""

data=cgi.FormContent()

ostype=data['type'][0]
port=data['port'][0]
memory=data['memory'][0]
size=data['size'][0]
flavour=data['flavour'][0]
name=data['uname'][0]

web_port=str(random.randint(5555,5899))


x=mariadb.connect(user='root',password='redhat',database='lw')

y=x.cursor()

sql="select port from iaas"

y.execute(sql)

result=y.fetchall()

for i in result:
	if(i[0]==port):
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/iaas_porterror.html\">\n")
		exit()





sql1="insert into iaas values(%s,%s,%s)"

y.execute(sql1,(name,port,web_port))
		
x.commit()

x.close()


commands.getstatusoutput("sudo qemu-img create -f qcow2 /images/{}.qcow2 {}G".format(name,size))


status=commands.getstatusoutput("sudo virt-install --hvm --name {} --memory {} --vcpus 1 --os-type {} --os-variant {} --cdrom /var/www/html/{}.iso --noautoconsole --disk /images/{}.qcow2,size={} --graphics vnc,listen=0.0.0.0,port={}".format(name,memory,ostype,flavour,flavour,name,size,port))


if(status[0]==0):
	
	commands.getstatusoutput("sudo /var/www/cgi-bin/websockify-master/run -D 192.168.43.112:{} 192.168.43.112:{}".format(web_port,port))
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/vnc/index.html?host=192.168.43.112&port={}\">\n".format(web_port)

else:
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/iaas_newuser.html\">\n")



	







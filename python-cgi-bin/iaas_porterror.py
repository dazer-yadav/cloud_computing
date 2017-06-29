#!/usr/bin/python2

import mysql.connector as mariadb
import cgi
import commands
import cgitb

cgitb.enable()

print "content-type:text/html"
print ""

data=cgi.FormContent()

ostype=data['type'][0]
port=data['port'][0]
memory=int(data['memory'][0])
size=int(data['size'][0])
flavour=data['flavour'][0]
name=data['uname'][0]

port_no=int(port)

x=mariadb.connect(user='root',password='redhat',database='lw')

y=x.cursor()

sql="select port from iaas"

y.execute(sql)

result=y.fetchall()

for i in result:
	if(i[0]==port):
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.93/iaas_porterror.html\">\n")
		exit()





sql1="insert into iaas values(%s,%s)"

y.execute(sql1,(name,port))
		
x.commit()

x.close()


commands.getstatusoutput("sudo qemu-img create -f qcow2 /images/{}.qcow2 {}G".format(name,size)


status=commands.getstatusoutput("sudo virt-install --hvm --name {} --memory {} --vcpus 1 --os-type {} --os-variant {} --cdrom /var/www/html/{}.iso --noautoconsole --disk /images/{}.qcow2,size={} --graphics vnc,listen=0.0.0.0,port={}".format(name,memory,ostype,flavour,flavour,name,size,port_no))


if(status[0]==0):
	
	commands.getstatusoutput("sudo /var/www/cgi-bin/websockify-master/run -D 192.168.43.93:5555 192.168.43.93:{}".format(port_no))
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.93/vnc/index.html?host=192.168.43.93&port=5555\">\n"

else:
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.93/iaas_porterror.html\">\n")



	







#!/usr/bin/python2

import cgi
import commands
import mysql.connector as mariadb
import cgitb

cgitb.enable()

print "content-type:text/html" #content header

print ""



def delete_obj():
	commands.getstatusoutput("sudo lvremove  /dev/combo/{} ".format(lv)) #for deleting malfunctioning lv
	
	

def create_obj(): #for creting lv,formatting and mounting
	status=commands.getstatusoutput("sudo lvcreate --name {} --size {}G /dev/combo ".format(lv,amount))
	if(status[0]==0):
		status=commands.getstatusoutput("sudo mkfs.ext4 /dev/combo/{}".format(lv))
		print status

		if(status[0]==0):
			commands.getstatusoutput("sudo mkdir /media/{}".format(lv))
			commands.getstatusoutput("sudo mount /dev/combo/{} /media/{}".format(lv,lv))
		else:
			delete_obj()
			create_obj()
	else:
		create_obj()


def delete_block():
	commands.getstatusoutput("sudo lvremove  /dev/combo1/{} ".format(lv))	


def create_block():
	status=commands.getstatusoutput("sudo lvcreate --name {} --size {}G /dev/combo1".format(lv,amount))
	if(status[0]==0):
		commands.getstatusoutput("sudo touch /etc/tgt/conf.d/{}.conf".format(lv))
		commands.getstatusoutput("sudo chmod 777 /etc/tgt/conf.d/{}.conf".format(lv))
		fh=open("/etc/tgt/conf.d/{}.conf".format(lv),mode='w')
		fh.write("<target {}>\n".format(lv))
		fh.write("backing-store /dev/combo1/{}\n".format(lv))
		fh.write("</target>\n")
		fh.close()
		
		commands.getstatusoutput("sudo setenforce 0")
		commands.getstatusoutput("sudo iptables -F")
		commands.getstatusoutput("sudo systemctl stop firewalld")
		commands.getstatusoutput("sudo systemctl restart tgtd")
		
	else:
		delete_block()
		create_block()
	
			
		


data=cgi.FormContent()

lv=data['mount_point'][0]#name of lv,mounted folder in server and that in client would be same as 'mount_point'
storage=data['type'][0]	#type=block or object
amount=int(data['amount'][0]) #amount.eg;2G


if(storage=='object'): 
	
	x=mariadb.connect(user='root',password='redhat',database='lw')

	y=x.cursor()

	sql="select user from common_users where user=%s;"

	y.execute(sql,(lv,))

	result=y.fetchone()

	trigger=str(result)

	if(trigger=='None'): 

		sql=("insert into common_users values(%s);")

		y.execute(sql,(lv,))

		x.commit()

		x.close()
		
		commands.getstatusoutput("sudo useradd {} ".format(lv))#username same as lv
		commands.getstatusoutput("sudo echo object |sudo passwd {} --stdin ".format(lv))#password bydefault object for all

	else:
		pass			
	

	create_obj()
	commands.getstatusoutput("sudo chown {} /media/{} ".format(lv,lv))#change ownership of mounted folder 
	commands.getstatusoutput("sudo chmod 700 /media/{}".format(lv))#change rwx
	

	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/object.html\">\n") #redirect to download page


elif(storage=='block'):
	create_block()
	print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/block.html\">\n")


		
	
	
	
		







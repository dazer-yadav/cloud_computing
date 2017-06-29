#!/usr/bin/python2

import cgi
import commands
import os
import cgitb

cgitb.enable()

print "content-type:text/html"

print ""


data=cgi.FormContent()

lv=data['mount_point'][0]
trigger=data['feedback'][0]

if(lv):
	commands.getstatusoutput("sudo touch {}_obj.py".format(lv))
	commands.getstatusoutput("sudo chmod 777 {}_obj.py".format(lv))
	commands.getstatusoutput("sudo chmod +x {}_obj.py".format(lv))
	fh=open('{}_obj.py'.format(lv),mode='w')
	fh.write("#!/usr/bin/python2\n")
	fh.write("import os\n")
	fh.write("os.system('yum install fuse-sshfs')\n")
	fh.write("os.system('mkdir /media/{}')\n".format(lv))
	fh.write("os.system('setenforce 0')\n")
	fh.write("os.system('iptables -F')\n")
	fh.write("os.system('systemctl stop firewalld')\n")
	fh.write("#your required password is object\n")
	fh.write("os.system('sshfs {}@192.168.122.165:/media/{} /media/{}')\n".format(lv,lv,lv))
	fh.write("raw_input()")
	fh.close()

	status=commands.getstatusoutput(" sudo tar -cvf /var/www/html/{}_obj.tar {}_obj.py".format(lv,lv))
	if(status[0]==0):
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/{}_obj.tar\">\n".format(lv))

	else:
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/object.html\">\n")


	
	
	

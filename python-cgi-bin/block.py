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
	commands.getstatusoutput("sudo touch {}_block.py".format(lv))
	commands.getstatusoutput("sudo chmod 777 {}_block.py".format(lv))
	commands.getstatusoutput("sudo chmod +x {}_block.py".format(lv))
	fh=open('{}_block.py'.format(lv),mode='w')
	fh.write("#!/usr/bin/python2\n")
	fh.write("import os\n")
	fh.write("os.system('yum install iscsi-initiator-utils')\n")
	fh.write("os.system('iscsiadm --mode discoverydb --type sendtargets --portal 192.168.122.165 --discover')\n")
	fh.write("os.system('iscsiadm --mode node --targetname {} --portal 192.168.122.165:3260 --login')\n".format(lv))
	fh.write("os.system('setenforce 0')\n")
	fh.write("os.system('iptables -F')\n")
	fh.write("os.system('systemctl stop firewalld')\n")
	fh.close()

	status=commands.getstatusoutput(" sudo tar -cvf /var/www/html/{}_block.tar {}_block.py".format(lv,lv))
	if(status[0]==0):
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/{}_block.tar\">\n".format(lv))

	else:
		print ("<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.122.165/block.html\">\n")


	
	
	

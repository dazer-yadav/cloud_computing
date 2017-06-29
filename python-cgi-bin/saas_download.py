#!/usr/bin/python2

import cgi
import cgitb
import commands
import mysql.connector as mariadb

cgitb.enable()

print "content-type:text/html"

print ""

data=cgi.FormContent()

user=data['uname'][0]
service=data['service'][0]

fh=open("/var/www/cgi-bin/{}_saas.py".format(user),mode='w')
fh.write("#!/usr/bin/python2\n")
fh.write("import os\n")
fh.write("os.system('yum install openssh-clients')\n")
fh.write("os.system('systemctl restart sshd')\n")
fh.write("os.system('sshpass -p object ssh -X {}@192.168.43.112 {}')\n".format(user,service))
fh.close()
commands.getstatusoutput("sudo chmod +x {}_saas.py".format(user))

status=commands.getstatusoutput("sudo tar -cvf /var/www/html/{}_{}.tar {}_saas.py".format(user,service,user))

if(status[0]==0):
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/{}_{}.tar\">\n".format(user,service)

else:
	print "<META HTTP-EQUIV=refresh CONTENT=\"0;URL=http://192.168.43.112/saas_download.html\">\n"






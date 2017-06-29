#!/usr/bin/python2
import os
os.system('yum install openssh-clients')
os.system('systemctl restart sshd')
os.system('sshpass -p object ssh -X nandi@192.168.43.112 firefox')

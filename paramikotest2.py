import paramiko
import sys
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
if len(sys.argv) != 2:
    print("Usage %s <filename>" % sys.argv[0])
    quit()
 
try:
    fd = open(sys.argv[1], "r")
except IOError:
    print("Couldn't open %s" % sys.argv[1])
    quit()
 
username,passwd = fd.readline().strip().split(":") #TODO: add error checking!
 
try:
    ssh.connect('localhost', username=username, password=passwd)
    stdin,stdout,stderr = ssh.exec_command("ls /tmp")
    for line in stdout.readlines():
        print(line.strip())
    ssh.close()
except paramiko.AuthenticationException:
    print("Authentication Failed")
    quit()
except:
    print("Unknown error")
    quit()
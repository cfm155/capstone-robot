import paramiko
from time import sleep
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
        ssh.connect('ev3dev.local', username='robot', password='maker')
except paramiko.SSHException:
        print("Connection Failed")
        quit()
 
stdin,stdout,stderr = ssh.exec_command("python3 onemotor.py")
#sleep(5)
#stdin,stdout,stderr = ssh.exec_command("hello")
#sleep(1)
#stdin.write("hello\n")
#sleep(1)
#sleep(10)
#stdin.write("x")
for line in stdout.readlines():
        print(line.strip())
ssh.close()
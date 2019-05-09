import paramiko
from time import sleep
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
        ssh.connect('ev3dev.local', username='robot', password='maker')
except paramiko.SSHException:
        print("Connection Failed")
        quit()
 
ssh.exec_command("touch object.txt")
#stdin,stdout,stderr = ssh.exec_command("hello")
#sleep(1)
#stdin.write("hello\n")
#sleep(1)
#sleep(10)
#stdin.write("x")
ssh.close()

# ssh.exec_command("python3 runaround.py")

ssh.close()
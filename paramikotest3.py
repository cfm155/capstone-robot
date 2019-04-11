import paramiko
 
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('ev3dev.local', username='robot', password='maker')
except paramiko.SSHException:
    print("Connection Error")
sftp = ssh.open_sftp()
sftp.cd("/tmp/")
print sftp.ls()
ssh.close()
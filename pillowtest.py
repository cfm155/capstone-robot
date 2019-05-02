from PIL import Image, ImageFilter
import os
import paramiko
from time import sleep
os.system("imagesnap plzwork.jpg\nconvert snapshot*.jpg plzwork.bmp\nrm snapshot*.jpg")
im = Image.open("plzwork.bmp")
rgb_im = im.convert('RGB')
r, g, b = rgb_im.getpixel((1, 1))
wbord= 600
hbord= 300

print(r, g, b)
(65, 100, 137)
print(im.format, im.size, im.mode)
box = (wbord, hbord, im.size[0] - wbord, im.size[1] - hbord)
region = im.crop(box)
region1 = region.filter(ImageFilter.BLUR)
region.show()
region1.show()

pixels = list(region.getdata())
reds = [i[0] for i in pixels]
greens = [i[1] for i in pixels]
blues = [i[2] for i in pixels]

for i in range(len(pixels)):
    if greens[i] > 75 and blues[i] > 75:
        reds[i] = 0

count = 0
for i in reds:
    if i > 0:
        count +=1
percRed = count*100/len(reds)
print(count, "avg reds: ", percRed)

# count = 0
# for i in greens:
#     if i > 75:
#         count +=1
# print(count, "avg greens: ", count*100/len(reds))
#
# count = 0
# for i in blues:
#     if i > 75:
#         count +=1
# print(count, "avg blues: ", count*100/len(reds))
print(max(reds), min(reds))
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('ev3dev.local', username='robot', password='maker')
except paramiko.SSHException:
    print("Connection Failed")
    quit()

if percRed > 20:
    stdin,stdout,stderr = ssh.exec_command("python3 beeptest.py")
    for line in stdout.readlines():
        print(line.strip())
else:
    print("no object detected :)")
ssh.close()
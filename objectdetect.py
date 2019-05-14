from PIL import Image, ImageFilter
import os
import paramiko
import time

# Use paramiko to connect to the robot through ssh
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('ev3dev.local', username='robot', password='maker')
except paramiko.SSHException:
    print("Connection Failed")
    quit()

# set threshold for how high the red value must be to count towards the percent of red pixels
redThreshold = 100

# set threshold for how low the green and blue values must be to count towards the percent of red pixels
threshold = 75

# set the minimum percent of red pixels to determine there is an object in the robot's path
percThreshold = 25

# set values for how large of a subrectangle you want the robot to look at. These values catch only what is in front
# of the robot.
top = 400
bottom = 200
left = 650
right = 650

# set how many images you want the robot to take, this value lasts about as long as the robot's followandavoid method.
steps = 45

# execute the runaroundrevised function on the actual robot
ssh.exec_command("python3 followandavoid.py")

# keep track of how long it takes for each picture to be taken and analyzed
startTime = time.time()
for step in range(steps):
    currtime = time.time()

    # take an image, convert it to a bmp, then delete the original image
    os.system("imagesnap\nconvert snapshot*.jpg check.bmp\nrm snapshot*.jpg")

    # open the new bmp image
    im = Image.open("check.bmp")

    # create a "box" with dimensions that we initialized earlier, then crop the rest
    box = (left, top, im.size[0] - right, im.size[1] - bottom)
    region = im.crop(box)

    # region = region.filter(ImageFilter.BLUR) # Gaussian blur the image (found that it did not help consistency of object detection)
    # region.show() # show the image if you'd like to see what the robot sees

    # take the rgb values of each pixel and separate them into red, blue, and green arrays
    pixels = list(region.getdata())
    reds = [i[0] for i in pixels]
    greens = [i[1] for i in pixels]
    blues = [i[2] for i in pixels]

    # in each pixel, check if the green/blue values are low enough, if not, set the red value to 0 to ensure it is not
    # counted towards the percent of reds
    for i in range(len(pixels)):
        if greens[i] > threshold and blues[i] > threshold:
            reds[i] = 0

    count = 0

    # check what reds are left, and if they're high enough, count them
    for i in reds:
        if i > redThreshold:
            count +=1
    # find the percent of reds in the image by dividing the count by the total number of pixels, then multiplying by 100
    percRed = count*100/len(reds)
    print("percent of reds:", percRed)

    # If the percent of red pixels in the image is high enough, send the robot a command that will create an object.txt
    # file if one does not exist, and will pause this program until that action is complete
    if percRed > percThreshold:
        print("object detected, sending command!")
        stdin,stdout,stderr = ssh.exec_command("touch object.txt")
        for line in stdout.readlines():
            print(line.strip())
    # if no object is detected, move on in the loop and take the next picture
    else:
        print("no object detected")
    print("time spent for step ",step,": ", time.time() - currtime)
    print()

# print out the time spent and close the ssh connection
timeSpent = time.time() - startTime
print("time spent for ", steps, "steps: ", timeSpent)
ssh.close()
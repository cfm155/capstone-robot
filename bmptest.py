pic = open("testing.bmp", encoding = "latin1")
bytesss = list(map(ord,list(pic.read())))
i = 138
reds = [[0 for x in range(1080)] for y in range(1920)]
while i < 6220938:
	reds[(i-138)//3%1920][(i-138)//3//1920] = bytesss[i]
	i+=3
avgreds = [[0 for x in range(1080)] for y in range(1920)]
row = 2
col = 2
#for i in range(len(reds)):
#	for j in range(len(reds[0])):
#		print(reds[i][j],end = ' ')
#	print()
while row < len(reds) - 2:
	col = 2
	while col < len(reds[0]) - 2:
		total = 0
		i = -2
		while i < 3:
			j = -2
			while j < 3:
				total += reds[row + i][col + j]
				j += 1
			i += 1
		avg = total//25
		avgreds[row][col] = avg
		col += 1
	row += 1
ofile = open('new.bmp','wb')
filetowrite = []
for i in range(len(bytesss)):
	if i > 137 and (i-138) %3 == 0:
		ofile.write(bytes([avgreds[(i-138)//3%1920][(i-138)//3//1920]]))
	else:
		ofile.write(bytes([bytesss[i]]))
#ofile.write(filetowrite[0])
#ogbytes = ""
#for i in range(138):
#	ofile.write(bytes[i])

#for i in range(len(avgreds)):
#	for j in range(len(avgreds[0])):
#		print(avgreds[i][j],end = '\t')
#	print()
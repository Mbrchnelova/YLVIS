f = open("map_1999_70.dat", "r")
g = open("map_1999_conv.dat", "w")

lines = f.readlines()

i = 1
for line in lines:
	if i > 2:
		line = line.split(" ")
		string = line[0] + " " + line[1] + " " + line[2] + " " + str(float(line[3])/2.0) + "\n"
		g.write(string)
	else:
		g.write(line)
	i = i + 1
f.close()
g.close()

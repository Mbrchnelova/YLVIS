# This script will load .dat data and compute the magnetic reconnection rate


import sys
import math


very_small = 1e-40
very_large = 1e+40
mu_0 = 1.25663706e-6


def find_max_current_2d(jfield, coords):
	indx = -1
	maximum = very_small
	coords_maximum = [-1, -1]
	for i in range(0, len(jfield)):
		if abs(jfield[i]) > maximum:
			indx = i
			maximum = jfield[i] 
			coords_maximum = [coords[i][0],  coords[i][1]]

	return maximum, coords_maximum, indx

def find_max_current_3d(jfield, coords):
        indx = -1
        maximum = very_small
        coords_maximum = [-1, -1, -1]
        for i in range(0, len(jfield)):
                if abs(jfield[i]) > maximum:
                        indx = i
                        maximum = jfield[i]
                        coords_maximum = [coords[i][0],  coords[i][1],  coords[i][2]]

        return maximum, coords_maximum, indx


def find_where_j_is_jmaxover2_2d(jmax, jfield, xcoord_jmax, ycoord_jmax, coords, tolspatial, tolj):

        coords_jmaxovertwo = []	
	jmaxovertwo = 0.0
        for i in range(0, len(jfield)):
                if abs(coords[i][0] - xcoord_jmax) < tolspatial:
			if abs(jfield[i] - jmax/2.0) < tolj:
				if coords[i][1] > ycoord_jmax:
					indx = i
					coords_jmaxovertwo = [coords[i][0],  coords[i][1]] 
					jmaxovertwo = jfield[i]
	return coords_jmaxovertwo, indx, jmaxovertwo


def find_where_j_is_jmaxover2_3d(jmax, jfield, xcoord_jmax, zcoord_jmax, coords, tolspatial, tolj):

        coords_jmaxovertwo = []
        jmaxovertwo = 0.0
        for i in range(0, len(jfield)):
                distance = ((coords[i][0] - xcoord_jmax)**0.5 + (coords[i][2] - zcoord_jmax)**2)**0.5
                if distance < tolspatial:
                        if abs(jfield[i] - jmax/2.0) < tolj:
                                indx = i
                                coords_jmaxovertwo = [coords[i][0],  coords[i][1]]
                                jmaxovertwo = jfield[i]
        return coords_jmaxovertwo, indx, jmaxovertwo


def compute_j_from_curl_B_2D(coords, Bx_data, By_data, Bz_data):

	Bx_curl = []
	By_curl = []
	Bz_curl = []

	for e in range(0, len(coords)):
		e_x = coords[e][0]
		e_y = coords[e][1]

		dy_min = very_large
		dy_max = very_small

                dx_min = very_large
                dx_max = very_small

		ind_y_min = -1
                ind_x_min = -1
                ind_y_max = -1
                ind_x_max = -1

		if e%1000 == 0:
			print "Cell ", e, " out of ", len(coords), " computed."


		# Search for the nearest neighbours now
		for f in range(0, len(coords)):
			f_x = coords[f][0]
                        f_y = coords[f][1]

			if (e != f):
				if (f_x - e_x) < dx_max and (f_x - e_x) > 0.0:
					dx_max = (f_x - e_x)
					ind_x_max = f

                                if (f_y - e_y) < dy_max and (f_y - e_y) > 0.0:
                                        dy_max = (f_y - e_y)
                                        ind_y_max = f


                                if (e_x - f_x) < dx_min and (e_x - f_x) > 0.0:
                                        dx_min = (e_x - f_x)
                                        ind_x_min = f


                                if (e_y - f_y) < dy_min and (e_y - f_y) > 0.0:
                                        dy_min = (e_y - f_y)
                                        ind_y_min = f

		# Now, for our current cell, the nearest cells in x and y directions are stored:
		# ind_x_max has the cell to the right 
		# ind_y_max has the cell upward
		# ind_x_min has the cell to the left
		# ind_y_min has the cell downward


		# For cells in the middle - not on the edges:
		if (ind_y_min > -1 and ind_y_max > -1 and ind_x_min > -1 and ind_x_max > -1):

			dx = coords[ind_x_max][0] -  coords[ind_x_min][0]
			dy = coords[ind_y_max][1] -  coords[ind_y_min][1]

			curl_Bx = 0.0 - (Bz_data[ind_y_max] - Bz_data[ind_y_min]) / dy
			curl_By = (Bz_data[ind_x_max] - Bz_data[ind_x_min]) / dx - 0.0 
			curl_Bz = (Bx_data[ind_y_max] - Bx_data[ind_y_min]) / dy - (By_data[ind_x_max] - By_data[ind_x_min]) / dx


			Bx_curl.append(curl_Bx/mu_0)
                        By_curl.append(curl_By/mu_0)
                        Bz_curl.append(curl_Bz/mu_0)


		# For cells on the edges:
		else:

			if ind_x_min > -1:
				dx = e_x - coords[ind_x_min][0] 
				Bx_in_x = Bx_data[ind_x_min]
                                By_in_x = By_data[ind_x_min]
                                Bz_in_x = Bz_data[ind_x_min]

			else:
                                dx = e_x - coords[ind_x_max][0]
                                Bx_in_x = Bx_data[ind_x_max]
                                By_in_x = By_data[ind_x_max]
                                Bz_in_x = Bz_data[ind_x_max]

			if ind_y_min > -1:
                                dy = e_y - coords[ind_y_min][1]
                                Bx_in_y = Bx_data[ind_y_min]
                                By_in_y = By_data[ind_y_min]
                                Bz_in_y = Bz_data[ind_y_min]

			else:
                                dy = e_y - coords[ind_y_max][1]
                                Bx_in_y = Bx_data[ind_y_max]
                                By_in_y = By_data[ind_y_max]
                                Bz_in_y = Bz_data[ind_y_max]

                        Bx = Bx_data[e]
                        By = By_data[e]
                        Bz = Bz_data[e]

                        curl_Bx = 0.0 - (Bz - Bz_in_y) / dy
			curl_By = (Bz - Bz_in_x) / dx - 0.0
			curl_Bz = (Bx - Bx_in_y) / dy - (By - By_in_x) / dx

                        Bx_curl.append(curl_Bx/mu_0)
                        By_curl.append(curl_By/mu_0)
                        Bz_curl.append(curl_Bz/mu_0)


	return Bx_curl, By_curl, Bz_curl

if (len(sys.argv)) < 2:
        print "Please provide geometry information."
if (len(sys.argv)) < 3:
        print "Please provide input datafilename information."
if (len(sys.argv)) < 4:
        print "Please provide output datafilename information."

#print str(sys.argv)
datafile = (sys.argv)[2]
geom = (sys.argv)[1]
datacurl = (sys.argv)[3]

if geom == '3d':
        is3d = True
elif geom == '2d':
        is3d = False
else:
        print "Warning, unrecognized geometry. Using 2d."
        is3d = False



# Using readlines() 
file1 = open(datafile, 'r')

Bxstring = "Bx"
Bystring = "By"
Bzstring = "Bz"
Ezstring = "Ez"
jstring = "Jz"
ustring = "U0"
rhonstring = "rho0"
rhoistring = "rho1"

Lines = file1.readlines() 
  
count = 0
novars = 0
noelems = 0
jindex = -1

Bxindex = -1
Byindex = -1
Bzindex = -1
Ezindex = -1
rhonindex = -1
rhoiindex = -1
uindex = -1

START_COORDS = False
START_DATA = False
data_line = -1

j_data = []
Bx_data = []
By_data = []
Bz_data = []
Ez_data = []
rhon_data = []
rhoi_data = []
u_data = []

data_index = 0

x_data = []
y_data = []
z_data = []
coords = []
xindex = 1
yindex = 2
zindex = 3

if (is3d):
	ndim = 3
else:
	ndim = 2

# Strips the newline character 
for line in Lines: 
	if len(line) > 0:
		count = count + 1
 	line_split = line.split(" ")



        if len(line_split) > 1:
                for section in range(0, len(line_split)):
                        if len(line_split[section]) > 0:
                                #print "line_split[section][0]", line_split[section][0]
                                if line_split[section][1:-1] == Bxstring:
                                        Bxindex = section - 2
					Bxindex = Bxindex - ndim
                                if line_split[section][1:-1] == Bystring:
                                        Byindex = section - 2
                                        Byindex = Byindex - ndim

                                if line_split[section][1:-1] == Bzstring:
                                        Bzindex = section - 2
                                        Bzindex = Bzindex - ndim

                                if line_split[section][1:-1] == Ezstring:
                                        Ezindex = section - 2
                                        Ezindex = Ezindex - ndim

                                if line_split[section][1:-1] == rhoistring:
                                        rhoiindex = section - 2
                                        rhoiindex = rhoiindex - ndim

                                if line_split[section][1:-1] == rhonstring:
                                        rhonindex = section - 2
                                        rhonindex = rhonindex- ndim

                                if line_split[section][1:-1] == ustring:
                                        uindex = section - 2
                                        uindex = uindex- ndim



        if line_split[0][1:len(Bxstring)+1] == Bxstring:
                Bxindex = count - 1

        if line_split[0][1:len(Bystring)+1] == Bystring:
                Byindex = count - 1

        if line_split[0][1:len(Bzstring)+1] == Bzstring:
                Bzindex = count - 1

        if line_split[0][1:len(Ezstring)+1] == Ezstring:
                Ezindex = count - 1

        if line_split[0][1:len(rhoistring)+1] == rhoistring:
                rhoiindex = count - 1

        if line_split[0][1:len(rhonstring)+1] == rhonstring:
                rhonindex = count - 1

        if line_split[0][1:len(ustring)+1] == ustring:
                uindex = count - 1

	if line_split[0] == "ZONE":
		novars = count - 2 # The ZONE line no longer contains the variables, nor does the header



        if START_DATA:


                line_data = []
                for i in range(0, len(line_split)):
                        if len(line_split[i]) > 0:
                                line_data.append(line_split[i])


                if data_index >= (Bxindex - 1) * noelems and data_index < (Bxindex) * noelems:
                        for section in range(0, len(line_data)):
                                Bx_data.append(float(line_data[section]))

                if data_index >= (Byindex - 1) * noelems and data_index < (Byindex) * noelems:
                        for section in range(0, len(line_data)):
                                By_data.append(float(line_data[section]))

                if data_index >= (Bzindex - 1) * noelems and data_index < (Bzindex) * noelems:
                        for section in range(0, len(line_data)):
                                Bz_data.append(float(line_data[section]))

                if data_index >= (Ezindex - 1) * noelems and data_index < (Ezindex) * noelems:
                        for section in range(0, len(line_data)):
                                Ez_data.append(float(line_data[section]))

                if data_index >= (rhonindex - 1) * noelems and data_index < (rhonindex) * noelems:
                        for section in range(0, len(line_data)):
                                rhon_data.append(float(line_data[section]))

                if data_index >= (rhoiindex - 1) * noelems and data_index < (rhoiindex) * noelems:
                        for section in range(0, len(line_data)):
                                rhoi_data.append(float(line_data[section]))

                if data_index >= (uindex - 1) * noelems and data_index < (uindex) * noelems:
                        for section in range(0, len(line_data)):
                                u_data.append(float(line_data[section]))

                data_index = data_index + len(line_data)


	if START_COORDS:

		line_data = []
		for i in range(0, len(line_split)):
			if len(line_split[i]) > 0:
				line_data.append(line_split[i])

		#data_index = data_index + len(line_data)
                if data_index >= (xindex - 1) * nonodes and data_index < (xindex) * nonodes:
                        for section in range(0, len(line_data)):
                                x_data.append(float(line_data[section]))

                if data_index >= (yindex - 1) * nonodes and data_index < (yindex) * nonodes:
                        for section in range(0, len(line_data)):
                                y_data.append(float(line_data[section]))

			if data_index == (yindex) * nonodes - 1 and not(is3d):
				START_DATA = True
				data_index = 0
				START_COORDS = False

 
                if (is3d):
                        if data_index >= (zindex - 1) * nonodes and data_index < (zindex) * nonodes:
                                for section in range(0, len(line_data)):
                                        z_data.append(float(line_data[section]))

				if data_index == (zindex) * nonodes - 1:
        	                        START_DATA = True
                	                data_index = 0
                        	        START_COORDS = False

		if not(START_DATA):
               		data_index = data_index + len(line_data)



	if len(line_split) > 1:
		# print "mhere"
		for section in range(0, len(line_split)):
			#if count < 50:
			#	print line_split[section][0:3]
			if line_split[section][0:8] == "Elements":
				line_split_split = line_split[section].split("=")
				noelems = (line_split_split[1].split(","))[0]
			 	noelems = int(noelems)	
			if line_split[section][0:2] == "DT":
				START_COORDS = True
				data_line = count

                        if line_split[section][0:4] == "ZONE":
                                START_COORDS = True
                                data_line = count

                        if line_split[section][0:1] == "E":
                                line_split_split = line_split[section].split("=")
                                noelems = (line_split_split[1].split(","))[0]
                                noelems = int(noelems)

                        if line_split[section][0:1] == "N":
                                line_split_split = line_split[section].split("=")
                                nonodes = (line_split_split[1].split(","))[0]
                                nonodes = int(nonodes)
				#print "nonodes", nonodes
				#print "Bxindex", Bxindex
                                #print "Byindex", Byindex
                                #print "Bzindex", Bzindex
                                #print "Ezindex", Ezindex
	
file1.close()

#print "xs: ", x_data
#print "ys: ", y_data
#print "Bx: ", Bx_data
#print "By: ", By_data
#print "Bz: ", Bz_data
#print "Ez: ", Ez_data


#print "Loaded ", novars, " variables and ", noelems, " elements."
#print "The domain is ", min(x_data), "-", max(x_data),  "x", min(y_data), "-", max(y_data)

#print "Checking variable order..."
#print "Bx found with order: ", Bxindex
#print "By found with order: ", Byindex
#print "Bz found with order: ", Bzindex
#print "Ez found with order: ", Ezindex
#print "rhon found with order: ", rhonindex
#print "rhoi found with order: ", rhoiindex

jx = []
jy = []
jz = []

#print "len(Bx_data): ", len(Bx_data)
#print "len(By_data): ", len(By_data)
#print "len(Bz_data): ", len(Bz_data)
#print "len(Ez_data): ", len(Ez_data)


file1 = open(datacurl, 'r') 
Lines = file1.readlines()

START_TIME = False
STOP_TIME = False
time = ""
for l in range(5, len(datacurl)-1):
        if datacurl[l-5:l] == "time_":
                START_TIME = True
	if START_TIME and not STOP_TIME:
		if datacurl[l+1] == ".":
			STOP_TIME = True
		time = time + str(datacurl[l])
	#if datacurl[l-5:l] == "time_":
	#	START_TIME = True
n = 1

'''
for line in Lines:
	
	if (n <= noelems):
		jx.append(float(line)/mu_0)	
        elif (n <= 2*noelems):
                jy.append(float(line)/mu_0)
	else:
                jz.append(float(line)/mu_0)
	n = n + 1
'''
connectivity = []
c = []
START_DATA  = False
for line in Lines:
	if START_DATA:
		line_split = line.split(" ")
		for s in range(0, len(line_split)):
			if len(line_split[s]) > 0 and n <= noelems: 
				jz.append(float(line_split[s])/mu_0)
				n = n + 1


			else:
				if len(line_split[s]) > 0:
					c.append(int(line_split[s]))
		if n > noelems:
			if len(c) > 0:
				connectivity.append(c)
			c = []

	if line[0:3] == " DT":
		START_DATA = True


	
x_elems = []
y_elems = []
z_elems = []


#print "len(x_data): ", len(x_data)

for e in range(0, noelems):
	n_1 = connectivity[e][0]
        n_2 = connectivity[e][1]
        n_3 = connectivity[e][2]
        n_4 = connectivity[e][3]

	e_x = x_data[n_1 - 1]*0.25 
        e_x += x_data[n_2 - 1]*0.25
        e_x += x_data[n_3 - 1]*0.25
        e_x += x_data[n_4 - 1]*0.25

	x_elems.append(e_x)

        e_y = y_data[n_1 - 1]*0.25
        e_y += y_data[n_2 - 1]*0.25
        e_y += y_data[n_3 - 1]*0.25
        e_y += y_data[n_4 - 1]*0.25

        y_elems.append(e_y)




for i in range(0, len(x_elems)):
        if (is3d):
                coords.append([x_elems[i], y_elems[i]], z_elems[i])
        else:
                coords.append([x_elems[i], y_elems[i]])




#if (len(jz) != len(jx) or len(jz) != len(jy)):
#	print "Corrupted curl data file. Inaccurate results."


#print "jz vs coords", len(jz), len(coords) 
'''
jx, jy, jz = compute_j_from_curl_B_2D(coords, Bx_data, By_data, Bz_data)
'''

j_data = jz

if (is3d):
        j_maximum, coords_j_maximum, indx_j_maximum = find_max_current_3d(j_data, coords)
else:
	j_maximum, coords_j_maximum, indx_j_maximum = find_max_current_2d(j_data, coords)


#print "Max of Jz found at: ", coords_j_maximum, " of ", j_maximum, " at index ", indx_j_maximum


#print "Index of j maximum: ", indx_j_maximum
#print "Length of Ez:", len(Ez_data)

#print "Length of coords:", len(coords)

Ez_star = Ez_data[indx_j_maximum]

x_coord_null = x_elems[indx_j_maximum]

tolj = j_maximum/10.0


# Currently, this functions to find the B* field in the y axis!! Even when 3D is chosen. 
# To change the axis in which we search for B*, change the functions correspondingly. 

if (is3d):
        tolspatial = max(abs(x_elems[1] - x_elems[0]),abs(z_data[1] - z_data[0])) /100.
        coords_jmaxovertwo, indx_jmaxovertwo, j_maxovertwo = find_where_j_is_jmaxover2_3d(j_maximum, j_data, coords_j_maximum[0],  coords_j_maximum[2], coords, tolspatial, tolj)
else:
	tolspatial = abs(x_elems[1] - x_elems[0])/100.
	coords_jmaxovertwo, indx_jmaxovertwo, j_maxovertwo = find_where_j_is_jmaxover2_2d(j_maximum, j_data, coords_j_maximum[0], coords_j_maximum[1], coords, tolspatial, tolj)


#print "Jmax/2 found at ", coords_jmaxovertwo," of ", j_maxovertwo, " at index ", indx_jmaxovertwo

B_up = Bx_data[indx_jmaxovertwo]**2 +  By_data[indx_jmaxovertwo]**2 +  Bz_data[indx_jmaxovertwo]**2
B_up = B_up**0.5

rhon_star = rhon_data[indx_jmaxovertwo]
rhoi_star = rhoi_data[indx_jmaxovertwo]

vA_star = B_up / math.sqrt(mu_0) / math.sqrt(rhon_star + rhoi_star)

M = Ez_star / vA_star / B_up

for u in range(0, len(u_data)):
	u_data[u] = float(u_data[u])

print time, "\t", M, "\t",  coords_jmaxovertwo[1] - coords_j_maximum[1], "\t", max(u_data)

#print "R of ", datafile, " is ", M, " with jmax: ", j_maximum, "E*:", Ez_star, "and Bup: ", B_up, "null at: ", coords_j_maximum, "j half at: ", coords_jmaxovertwo, "of", j_maxovertwo

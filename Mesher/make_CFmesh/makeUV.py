import sys
import math


def isClose(val1, val2):
	if (abs(val1 - val2) < 1e-8):
		return True
	else:
		return False



def RemoveDoublePoints(rs, thetas, phis, xs, ys, zs, elements):
        nopoints = len(xs)
        noelems = len(elements)
        new_xs = []
        new_ys = []
        new_zs = []

        new_rs = []
        new_thetas = []
        new_phis = []

        new_elements = []

        replacements = []

        for i in range(0, nopoints):
                DUPLICATE = False
                for j in range(0, len(new_xs)):

			if thetas[i] == -90.0 or thetas[i] == 90.0:
                        	if thetas[i] == new_thetas[j] and rs[i] == new_rs[j]:
                        	        DUPLICATE = True
                        	        replacements.append(j)
                        	        #print "found a duplicate" 
                if not DUPLICATE:
                        new_rs.append(rs[i])
                        new_thetas.append(thetas[i])
                        new_phis.append(phis[i])
                        new_xs.append(xs[i])
                        new_ys.append(ys[i])
                        new_zs.append(zs[i])
                        replacements.append(-1)


        newlist = []
        index = 0
        for i in range(0, nopoints):
                if replacements[i] == -1:
                        newlist.append(index)
                        index = index + 1
                else:
                        replacement = replacements[i]
                        newlist.append(replacement)



        for e in range(0, noelems):
                for n in range(0, len(elements[e])): 
                        node = elements[e][n]
                        if replacements[node] != -1:

                                position = replacements[node]

                                elements[e][n] = newlist[node]
                        else:
                                elements[e][n] = newlist[node]

        return new_rs, new_thetas, new_phis, new_xs, new_ys, new_zs, elements



pi = 3.141592654


Rs1 = [1.0, 1.0005, 1.00156468, 1.00276709, 1.00412505, 1.00565869, 1.00739071, 1.0093468, 1.01155593, 1.01405085, 1.01686851, \
                1.02005068, 1.02364451, 1.02770324, 1.03228702, 1.03746378, 1.04331022, 1.04991298, 1.05736989, 1.06579145, 1.07530246, \
                1.08604384, 1.09817476, 1.11187497, 1.1273475, 1.1448216, 1.16455621, 1.18684376, 1.2120145, 1.24044141, 1.27254572, \
                1.30880316, 1.34975097, 1.39599594, 1.44822331, 1.50720699, 1.573821, 1.64905242, 1.73401603, 1.82997083, 1.93833865, \
                2.06072531, 2.19894431, 2.3550438, 2.53133683, 2.73043574, 2.95529074, 3.20923375, 3.49602769, 3.81992225, 4.18571691, \
                4.598832, 5.06538905, 5.5923015, 6.18737712, 6.85943373, 7.61842986, 8.47561228, 9.44368271, 10.536986, 11.7717227, \
                13.1661891, 14.74104838, 16.51963677, 18.52830936, 20.79683062, 22.0, 25.0, 30.0, 40.0, 50.0]



nlat0 = 36
nlong = 36
nrad = len(Rs1)






nlat = nlat0 + 3
lats = []
dtheta = 180.0/(nlat0)

for i in range(0, nlat):
	lats.append(0)

for i in range(2, nlat-2):
	theta = 90.0 - (i-1) * dtheta
	lats[i] = theta

print lats


lats[0] = 90.0
lats[-1] = -90
lats[1] = 89.5
lats[-2] = -89.5

print lats




points = []

np = 0
for i in range(0, nrad):
	for j in range(0, nlat):
		for k in range(0, nlong):


			points.append([i, j, k])
			np = np + 1



dphi = 360.0/(nlong)
dr = 1.0
r0 = 1.0




spherical = []
cartesian = []
xs = []
ys = []
zs = []

rs = []
thetas = []
phis = []
#initial point = 

print "Starting the computation of the mesh."
INSERTED_LOWER = False
INSERTED_UPPER = False
SKIP = False
for p in range(0, np):

	#//if INSERTED_LOWER and j == 0:
	#//	SKIP = True

	#if INSERTED_UPPER and j == nlat:
	#	SKIP = True

	i = points[p][0]
	j = points[p][1]
	k = points[p][2]

	r = Rs1[i] #r0 + i*dr
	#theta = 90.0 - j * dtheta

	theta = lats[j]
	phi = 0.0 + k * dphi

	spherical.append([r, theta, phi])

	phirad = phi * pi/180.0
	thetarad = theta * pi/180.0

	x = r * math.cos(phirad) * math.cos(thetarad)
	y = r * math.sin(phirad) * math.cos(thetarad)
	z = r * math.sin(thetarad)

	cartesian.append([x, y, z])

	xs.append(x)
	ys.append(y)
	zs.append(z)

	rs.append(r)
	thetas.append(theta)
	phis.append(phi)
	#if j == 0:
	#	INSERTED_LOWER = True

	#if j == nlat:
	#	INSERTED_UPPER = True


connectivity = []
inlet = []
outlet = []
ninlets = 0
noutlets = 0

print "Points generated. Creating connectivity."
for i in range(0, nrad-1):
	for j in range(0, nlat-1):
		for k in range(0, nlong):
	

			if k < nlong-1:

				node1 = k 	+ nlong * j 	+ nlong * nlat * i
				node4 = (k+1) 	+ nlong * j 	+ nlong * nlat * i
				node3 = (k+1) 	+ nlong * (j+1) + nlong * nlat * i
				node2 = k 	+ nlong * (j+1) + nlong * nlat * i

				node5 = k 	+ nlong * j 	+ nlong * nlat * (i+1)
				node8 = (k+1) 	+ nlong * j 	+ nlong * nlat * (i+1)
				node7 = (k+1) 	+ nlong * (j+1) + nlong * nlat * (i+1)
				node6 = k 	+ nlong * (j+1) + nlong * nlat * (i+1)
 
				cell = [node1, node2, node3, node4, node5, node6, node7, node8]
 
			else:
				node1 = k       + nlong * j     + nlong * nlat * i
				node4 = (0) 	+ nlong * j     + nlong * nlat * i
				node3 = (0)     + nlong * (j+1) + nlong * nlat * i
				node2 = k       + nlong * (j+1) + nlong * nlat * i

				node5 = k       + nlong * j     + nlong * nlat * (i+1)
				node8 = (0)     + nlong * j     + nlong * nlat * (i+1)
				node7 = (0)     + nlong * (j+1) + nlong * nlat * (i+1)
				node6 = k       + nlong * (j+1) + nlong * nlat * (i+1)

				cell = [node1, node2, node3, node4, node5, node6, node7, node8]


			if i == 0:
				inlet.append(1)
				outlet.append(0)
				ninlets = ninlets + 1

			if i == nrad-2:
				outlet.append(1)
				inlet.append(0)
				noutlets = noutlets + 1

			if i > 0 and i < nrad-2:
				inlet.append(0)
				outlet.append(0)


			connectivity.append(cell)



print "Connectivity created. Removing double points."
#for i in range(0, np):
#	print cartesian[i], "\t", spherical[i], "\t", points[i]
new_rs, new_thetas, new_phis, new_xs, new_ys, new_zs, new_connectivity = RemoveDoublePoints(rs, thetas, phis, xs, ys, zs, connectivity)

#for i in range(0, len(new_connectivity)):
#	print new_connectivity[i]

ne = len(new_connectivity)

elements = []

nprisms = 0
hexas = []
prisms = []

print "Double points removed. Detecting prism elements."

for i in range(0, ne):

	element = new_connectivity[i]
	PRISM = False

	n1 = element[0]
	n2 = element[1]
	n3 = element[2]
	n4 = element[3]
	n5 = element[4]
	n6 = element[5]
	n7 = element[6]
	n8 = element[7]

	if n1 == n2 or n2 == n3 or n3 == n4 or n1 == n3 or n1 == n4 or n2 == n4:
		PRISM = True


	if PRISM == False:
		elements.append(element)
		hexas.append(True)
		prisms.append(False)
	else:
		if n1 == n2:
			prism_element = [n1, n3, n4, n5, n7, n8]
		elif n3 == n4:
			prism_element = [n1, n2, n3, n5, n5, n7]

		elif n2 == n3:
			prism_element = [n1, n2, n4, n5, n6, n8]

                elif n1 == n4:
                        prism_element = [n1, n2, n3, n5, n6, n7]
		else:
			print n1, n2, n3, n4, n5, n6, n7, n8
			print "you dumb fuck, think"

		elements.append(prism_element)
		nprisms = nprisms + 1 
		hexas.append(False)
		prisms.append(True)


nhexas = ne - nprisms
nnodes = len(new_xs)

print "Prisms detected. Formatting the outputfile."

f = open("testrealmid_limited_verybig.CFmesh", "w")


line ="!COOLFLUID_VERSION 2013.9" + "\n"
f.write(line)
line ="!CFMESH_FORMAT_VERSION 1.3" + "\n"
f.write(line)

line ="!NB_DIM 3" + "\n"
f.write(line)

line ="!NB_EQ 1" + "\n"
f.write(line)

line ="!NB_NODES " + str(nnodes) + " 0" + "\n"
f.write(line)

line ="!NB_STATES " + str(ne) + " 0" + "\n"
f.write(line)

line ="!NB_ELEM " + str(ne) + "\n"
f.write(line)

line ="!NB_ELEM_TYPES 2" + "\n"
f.write(line)

line ="!GEOM_POLYORDER 1" + "\n"
f.write(line)

line ="!SOL_POLYORDER 0" + "\n"
f.write(line)

line ="!ELEM_TYPES Hexa Prism" + "\n"
f.write(line)

line ="!NB_ELEM_PER_TYPE " + str(nhexas) + " " + str(nprisms) + "\n"
f.write(line)

line ="!NB_NODES_PER_TYPE 8 6" + "\n"
f.write(line)

line ="!NB_STATES_PER_TYPE 1 1" + "\n"
f.write(line)

line ="!LIST_ELEM" + "\n"
f.write(line)

count = 0
matching = []
for i in range(0, ne):
	if hexas[i]:
		el = elements[i]
		line = str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + " " + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + " " + str(el[6]) + " " + str(el[7]) + " " + str(count) + "\n"
		matching.append([i, count])
		count = count + 1
		f.write(line)

for i in range(0, ne):
	if prisms[i]:
		el = elements[i]
		line = str(el[0]) + " " + str(el[1]) + " " + str(el[2]) + " " + str(el[3]) + " " + str(el[4]) + " " + str(el[5]) + " " + str( count) + "\n"
		matching.append([i, count])
		count = count + 1
		f.write(line)

elements_reordered = []
inlets_reordered = []
outlets_reordered = []

for j in range(0, ne):
	elements_reordered.append([])
	inlets_reordered.append([])
	outlets_reordered.append([])

for j in range(0, ne):
	i = matching[j][0]
	count = matching[j][1]
        elements_reordered[count] = elements[i]        
	inlets_reordered[count] = inlet[i]
	outlets_reordered[count] = outlet[i]


line ="!NB_TRSs 2" + "\n"
f.write(line)

line ="!TRS_NAME Inlet" + "\n"
f.write(line)

line ="!NB_TRs 1" + "\n"
f.write(line)

line ="!NB_GEOM_ENTS " + str(ninlets) + "\n"
f.write(line)

line ="!GEOM_TYPE Face" + "\n"
f.write(line)

line ="!LIST_GEOM_ENT" + "\n"
f.write(line)

for i in range(0, ne):
	if inlet[i]:
		element = elements[i]
		for j in range(0, len(matching)):
			if matching[j][0] == i:
				count = matching[j][1]

		if len(element) == 8:
			line = str(4) + " " + str(1) + " " + str(element[0]) + " " + str(element[1]) + " " + str(element[2]) + " " + str(element[3]) + " " + str(count) + "\n"
		else:
			line = str(3) + " " + str(1) + " " + str(element[0]) + " " + str(element[1]) + " " + str(element[2]) + " " + str(count) + "\n"	
		f.write(line)



line ="!TRS_NAME Outlet" + "\n"
f.write(line)

line ="!NB_TRs 1" + "\n"
f.write(line)

line ="!NB_GEOM_ENTS " + str(noutlets) + "\n"
f.write(line)

line ="!GEOM_TYPE Face" + "\n"
f.write(line)

line ="!LIST_GEOM_ENT" + "\n"
f.write(line)

for i in range(0, ne):
        if outlet[i]:
                element = elements[i]

                for j in range(0, len(matching)):
                        if matching[j][0] == i:
                                count = matching[j][1]

                if len(element) == 8:
                        line = str(4) + " " + str(1) + " " + str(element[4]) + " " + str(element[5]) + " " + str(element[6]) + " " + str(element[7]) + " " + str(count) + "\n"
                else:
                        line = str(3) + " " + str(1) + " " + str(element[3]) + " " + str(element[4]) + " " + str(element[5]) + " " + str(count) + "\n"                        
                f.write(line)

line = "!EXTRA_VARS" + "\n"
f.write(line)
line = "!LIST_NODE" + "\n"
f.write(line)

for i in range(0, len(new_xs)):
	line = str(new_xs[i]) + " " + str(new_ys[i]) + " " + str(new_zs[i]) + "\n"
	f.write(line)


line = "!LIST_STATE 0" + "\n"
f.write(line)

line = "!END"+ "\n"
f.write(line)

f.close()






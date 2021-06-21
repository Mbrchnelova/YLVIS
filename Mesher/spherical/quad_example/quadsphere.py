import sys
import math
import copy
import datetime 

def RemoveDoublePoints(xs, ys, zs, elements):
	nopoints = len(xs)
	noelems = len(elements)
	new_xs = []
	new_ys = []
	new_zs = []
	new_elements = []
	replacements = []
	for i in range(0, nopoints):
		DUPLICATE = False
		for j in range(0, len(new_xs)):
			if xs[i]==new_xs[j] and ys[i]==new_ys[j] and zs[i]==new_zs[j]:
				DUPLICATE = True
				replacements.append(j)
		if not DUPLICATE:
			new_xs.append(xs[i])
			new_ys.append(ys[i])
			new_zs.append(zs[i])
			replacements.append(-1)
	#-1, -1, 0, -1, 2


	#print("replacements", replacements)

	newlist = []
	index = 0
	for i in range(0, nopoints):
		if replacements[i] == -1:
			newlist.append(index)
			index = index + 1
		else:
			replacement = replacements[i]
			newlist.append(replacement)


	#0 1 -1 2 -1

        #print("newlist", newlist)

	#replaced_list = []
	#for i in range(0, nopoints):
	#	if replacements[i] != -1:
	#		position = replacements[i]
	#		replaced_list.append(newlist[position])
	#	else:
	#		replaced_list.append(newlist[i])

	#0 1 0 
	#print("replaced_list", replaced_list)


	for e in range(0, noelems):
		for n in range(0, 4):
			node = elements[e][n]
			if replacements[node] != -1:
				position = replacements[node]
                                print("replacing",node,"with",replacements[node],"at",newlist[position])

				elements[e][n] = newlist[node]
			else:
				elements[e][n] = newlist[node]

	return new_xs, new_ys, new_zs, elements 

def RemoveDoubleElems(elements):
	new_elements = []
	noelems = len(elements)
	for i in range(0, noelems):
		DUPLICATE = False
		for j in range(0, len(new_elements)):
			if elements[i] == new_elements[j]:
				DUPLICATE = True
		if not DUPLICATE:
			new_elements.append(elements[i])

	return new_elements


#The following function takes the existing icosphere surface and normalises its dimension to 1
def Normalize(xs, ys, zs):
	nopoints = len(xs)
	xs_new = []
	ys_new = []
	zs_new = []
	for i in range(0, nopoints):
		r = (xs[i]**2 + ys[i]**2 + zs[i]**2)**0.5
		phi = math.atan2(ys[i],xs[i])
		theta = math.acos(zs[i]/r)

		x = 1.0 * math.sin(theta) * math.cos(phi)
		y = 1.0 * math.sin(theta) * math.sin(phi)
		z = 1.0 * math.cos(theta)

		xs_new.append(x)
		ys_new.append(y)
		zs_new.append(z)

	return xs_new, ys_new, zs_new


#The following function takes the existing icosphere surface and adjusts its dimension to r
def AdjustRadius(xs, ys, zs, r):
        nopoints = len(xs)
        xs_new = []
        ys_new = []
        zs_new = []
        for i in range(0, nopoints):
                r_current = (xs[i]**2 + ys[i]**2 + zs[i]**2)**0.5
                phi = math.atan2(ys[i],xs[i])
                theta = math.acos(zs[i]/r_current)

                x = r * math.sin(theta) * math.cos(phi)
                y = r * math.sin(theta) * math.sin(phi)
                z = r * math.cos(theta)
                            
                xs_new.append(x)
                ys_new.append(y)
                zs_new.append(z)
               
        return xs_new, ys_new, zs_new


#The following function adjusts the element indices of the icosphere elements based on which layer it is
def AdjustConnectivity(elems, nlayer, nopoints):
	new_elems = []
	last_elem = len(elems)
	for i in range(0, len(elems)):
		e1 = elems[i][0] + nlayer * nopoints
		e2 = elems[i][1] + nlayer * nopoints
		e3 = elems[i][2] + nlayer * nopoints
                e4 = elems[i][3] + nlayer * nopoints

		new_elems.append([e1, e2, e3, e4])

	return new_elems

#The following function creates a connectiivty between the first two layers of the mesh
def GetFirstConnectivity(elems, added_elems):
	nofaces = len(elems)
	connectivity = []

	for i in range(0, nofaces):
		#Old elem is the element from the base layer
		old_elem = elems[i]

		#Stacked elem is the element from the new layr
		stacked_elem = added_elems[i]
		oe1 = old_elem[0]
		oe2 = old_elem[1]
		oe3 = old_elem[2]
		oe4 = old_elem[3]

		se1 = stacked_elem[0]
		se2 = stacked_elem[1]
		se3 = stacked_elem[2]
		se4 = stacked_elem[3]
		#The connectivity exists between the old and stacked element
		prism = [oe1, oe2, oe3, oe4, se1, se2, se3, se4]
		connectivity.append(prism)		
	return connectivity

def GetConnectivity(old_connectivity, added_elems, nobasepoints):
	nofaces = len(added_elems)
	connectivity = []
	for i in range(0, nofaces):
                #Stacked elem is the element from the added layer
		se1 = added_elems[i][0] 
		se2 = added_elems[i][1]
		se3 = added_elems[i][2]
		se4 = added_elems[i][3]

                #Old elem is the element from the previous layer
		oe1 = added_elems[i][0] - nobasepoints
		oe2 = added_elems[i][1] - nobasepoints
		oe3 = added_elems[i][2] - nobasepoints
		oe4 = added_elems[i][3] - nobasepoints

		prism = [oe1, oe2, oe3, oe4, se1, se2, se3, se4]

		connectivity.append(prism)

	return connectivity


def StackFirstLayer(xs, ys, zs, r, delta_r, elems):
	#The total number of points corresponds to the length of the x-array
	nopoints = len(xs)

	#Find the new radius of the stacked layer
	new_r = r + delta_r

	#Generate the new set of points base on the original set
	added_xs, added_ys, added_zs = AdjustRadius(xs, ys, zs, new_r) 
	
	#Generate new element connectivities
	added_elems = AdjustConnectivity(elems, 1, nopoints)

	#Determine the connectivity of the triangular prisms
	connectivity = GetFirstConnectivity(elems, added_elems) 

	all_xs = xs + added_xs
	all_ys = ys + added_ys
	all_zs = zs + added_zs

	all_elems = elems + added_elems

	return all_xs, all_ys, all_zs, all_elems, connectivity



def StackLayer(xs, ys, zs, base_xs, base_ys, base_zs, r, delta_r, elems, base_elems, nobasepoints, nlayer, old_connectivity):
        #The total number of points corresponds to the length of the x-array
	nopoints = len(xs)
	#print("1old", old_connectivity)
	#Find the new radius of the stacked layer
	new_r = r + delta_r
	print("Adding layer at:", new_r)
	#Generate the new set of points
	added_xs, added_ys, added_zs = AdjustRadius(base_xs, base_ys, base_zs, new_r)


	#Generate new element connectivities
	added_elems = AdjustConnectivity(base_elems, nlayer, nobasepoints)

	#print("Added elems:", added_elems)

	#Determine the connectivity of the triangular prisms
	connectivity = GetConnectivity(old_connectivity, added_elems, nobasepoints)
	#print("2old", old_connectivity)
	#print("2New", connectivity)

	all_xs = xs + added_xs
	all_ys = ys + added_ys
	all_zs = zs + added_zs

	all_elems = elems + added_elems

	connectivity = old_connectivity + connectivity
	#print("3all", connectivity)
	return all_xs, all_ys, all_zs, all_elems, connectivity, added_elems


def ReturnSpacing(r):
	spacing = 1.0

	return spacing


def ReturnSpacing_idx(i):

	Rs = [1.0005, 1.00156468, 1.00276709, 1.00412505, 1.00565869, 1.00739071, 1.0093468, 1.01155593, 1.01405085, 1.01686851, \
		1.02005068, 1.02364451, 1.02770324, 1.03228702, 1.03746378, 1.04331022, 1.04991298, 1.05736989, 1.06579145, 1.07530246, \
		1.08604384, 1.09817476, 1.11187497, 1.1273475, 1.1448216, 1.16455621, 1.18684376, 1.2120145, 1.24044141, 1.27254572, \
		1.30880316, 1.34975097, 1.39599594, 1.44822331, 1.50720699, 1.573821, 1.64905242, 1.73401603, 1.82997083, 1.93833865, \
		2.06072531, 2.19894431, 2.3550438, 2.53133683, 2.73043574, 2.95529074, 3.20923375, 3.49602769, 3.81992225, 4.18571691, \
		4.598832, 5.06538905, 5.5923015, 6.18737712, 6.85943373, 7.61842986, 8.47561228, 9.44368271, 10.536986, 11.7717227, \
		13.1661891, 14.74104838, 16.51963677, 18.52830936, 20.79683062]

	spacing = Rs[i+1] - Rs[i] 

	return spacing

def Transform_Rsun(xs, ys, zs):
	tr_xs = copy.deepcopy(xs)
        tr_ys = copy.deepcopy(ys)
        tr_zs = copy.deepcopy(zs)
	Rsun = 696340000.
	for i in range(0, len(tr_xs)):
		tr_xs[i] = tr_xs[i] * Rsun
                tr_ys[i] = tr_ys[i] * Rsun
                tr_zs[i] = tr_zs[i] * Rsun 

	return tr_xs, tr_ys, tr_zs

def WriteMesh(path, name, block_type, elements, nodes, boundaries, ngrps, nbsets, ndfcd, ndfvl):
        SUCCESS = 0

        filename = path + name
        print("Writing to: ", filename)
        #The fist line is the control info data
        f = open(filename, "w")
        line = "        CONTROL INFO 2.4.6" + '\n'
        f.write(line)

        #The second line indicates that the output file should be .neu
        line = "** GAMBIT NEUTRAL FILE" + '\n'
        f.write(line)

        #The third line the mesh name
        line = "mesh" + '\n'
        f.write(line)

        #The fourth line the version of the programme
        line = "PROGRAM:                BRCHMESH     VERSION:  0.0.1" + '\n'
        f.write(line)

        #The fifth line is the date and time
        now = datetime.datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        line = dt_string  + '\n'
        f.write(line)

        #The sixth line the order of the neu mesh paramerets:
        #number of points
        #number of elements
        #number of element groups
        #number of BC sets
        #number of coordinate directions
        #number of fluid velocity directions
        line = "     NUMNP     NELEM     NGRPS    NBSETS     NDFCD     NDFVL" + '\n'
        f.write(line)


        line = str(len(nodes)) + '\n'
        f.write(line)

        line = str(len(elements))+ '\n'
        f.write(line)

        line = str(ngrps) + '\n'
        f.write(line)

        line = str(nbsets) + '\n'
        f.write(line)

        line = str(ndfcd) + '\n'
        f.write(line)

        line = str(ndfvl) + '\n'
        f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)


        #For the prism mesh, determine from the boundaries which one is inlet and which one the outlet
        if block_type == "prism":
                inlet = boundaries[0:int(len(boundaries)/2)]
                outlet = boundaries[int(len(boundaries)/2):-1]



        line = "   NODAL COORDINATES 2.4.6" + '\n'
        f.write(line)


        #Next, write all the node coordinates - for each node, the index and coordinates x, y (and z) separated by "\n"
        for n in range(0, len(nodes)):
                node = nodes[n]
                if block_type == "2d_rect_quad":
                        line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2])  + '\n'

                elif block_type == "3d_box_quad" or "prism":
                        line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2]) + '\n' + str(node[3])  + '\n'


                else:
                        sys.exit("Writing for the selected block type not yet implemented. Abording.")

                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = "      ELEMENTS/CELLS 2.4.6"  + '\n'
        f.write(line)


        #Next, also write the connectivity of the elements - for each element, its index and the nodex which it is composed of
        for e in range(0, len(elements)):
                ele = elements[e]

                if block_type == "2d_rect_quad":
                        line = str(ele[0]+1) + '\n' + str(2) + '\n' + str(4) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n'

                elif block_type == "3d_box_quad":
                        line = str(ele[0]+1) + '\n' + str(4) + '\n' + str(8) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n' + str(ele[5]+1) + '\n' + str(ele[6]+1) + '\n' + str(ele[7]+1) + '\n' + str(ele[8]+1) + '\n'

                elif block_type == "prism":
                        line = str(ele[0]+1) + '\n' + str(4) + '\n' + str(8) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n' + str(ele[5]+1) + '\n' +  str(ele[6]+1) + '\n' + str(ele[7]+1) + '\n' + str(ele[8]+1) + '\n'

                else:
                        sys.exit("Writing for the selected block type not yet implemented. Abording.")

                f.write(line)



        #For the spherical mesh, also add the inlet and outlet boundaries
        #if block_type == "prism":

        #        for b in range(0, len(boundaries)):
        #                boundary = boundaries[b]
        #                line = str(boundary[0]+1) + '\n' + str(3) + "\n" + str(3) + "\n" + str(boundary[2]+1) + "\n" + str(boundary[3]+1) + "\n" + str(boundary[4]+1) + "\n"
        #                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = "       ELEMENT GROUP 2.4.6"  + '\n'
        f.write(line)

        #Next, write up the physical groups - usually just one composed of all the elements and fluid material
        line = "GROUP:" + str(ngrps) + '\n'
        f.write(line)

        line = "ELEMENTS:" + str(len(elements)) + '\n'
        f.write(line)

        line = "MATERIAL:          2"  + '\n'
        f.write(line)

        line = "NFLAGS:          1" + '\n'
        f.write(line)

        line = "                           fluid" + '\n'
        f.write(line)


        left = len(elements)
        i = 0
        line = ""

        if block_type == "2d_rect_quad" or block_type == "3d_box_quad":
                for e in range(0, len(elements)):
                        ele = elements[e]
                        i = i + 1

                        if i > 9:
                                line = line + str(ele[0]+1)  + '\n'
                                i = 0
                                f.write(line)
                                line = ""

                        else:
                                line = line + str(ele[0]+1) + "\n"

        else: 
                #print("ll entities:", len(elements))
                for e in range(0, len(elements)):
                        ele = (elements)[e]
                        i = i + 1

                        if i > 9:
                                line = line + str(ele[0]+1)  + '\n'
                                i = 0
                                f.write(line)
                                line = ""

                        else:
                                line = line + str(ele[0]+1) + "\n"

        if len(line) > 0:
                f.write(line)

        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
        f.write(line)



        #Finally, document the boundaries or inlets/outlets into the domain
        if block_type == "2d_rect_quad":
                for flag in range(1, 5):

                        if flag == 1:
                                line = "x0" + '\n'

                        if flag == 3:
                                line = "x1" + '\n'

                        if flag == 2:
                                line = "y0" + '\n'

                        if flag == 4:
                                line = "y1" + '\n'

                        f.write(line)

                        count = 0
                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        count = count + 1

                        line = str(count) + '\n'
                        f.write(line)

                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0]
                                        line = str(el+1) + "\n" + str(3) + "\n" + str(flag)  + '\n'
                                        f.write(line)
                line = "ENDOFSECTION" + '\n'
                f.write(line)
                line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
                f.write(line)



        elif block_type == "prism":
                for flag in range(1, 3):

                        if flag == 1:
                                line = "Inlet" + '\n'

                        if flag == 2:
                                line = "Outlet" + '\n'


                        f.write(line)


                        count = 0

                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        count = count + 1

                        line = str(count) + '\n'
                        f.write(line)


                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0]

                                        if (flag == 1):
                                                side = 5
                                        else:
                                                side = 6
                                        line = str(el+1) + "\n" + str(4) + "\n" + str(side)  + '\n'
                                        f.write(line)

                line = "ENDOFSECTION" + '\n'
                f.write(line)
                line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
                f.write(line)


        else:
                sys.exit("Writing for the selected block type not yet implemented. Abording.")

        line = "ENDOFSECTION" + '\n'
        f.write(line)

        f.close()

        SUCCESS = 1
        return SUCCESS






















###################################################################################################
###################################################################################################



args = (sys.argv)
inputfile = args[1]
outputfile = args[2]


print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)


#Open the ply formatted base icosphere
#file1 = open("icosub_5.ply", "r")

file1 = open(inputfile, "r")

Lines = file1.readlines()

i = 0
ndata = 0
GET_DATA = False
xs = []
ys = []
zs = []
nxs = []
nys = []
nzs = []
nelems = 0
elems = []
GET_ELEM = False

#Load the data from the ply file
for line in Lines:


	#Extract the basic information
	words = line.split(" ")
	if i == 3:
		novertices = int(words[2])
	if i == 10:
		nfaces = int(words[2])
	if i >= 13:
		GET_DATA = True

	#Extract the node coordinates and normals
	if GET_DATA:

		if len(words) == 6:
			xs.append(float(words[0]))
			ys.append(float(words[1]))
			zs.append(float(words[2]))
			nxs.append(float(words[3]))
			nys.append(float(words[4]))
			nzs.append(float(words[5]))

		ndata = ndata + len(words)

		if ndata > 6*novertices:
			GET_ELEM = True
			GET_DATA = False

	#Extract the element connectivities
	if GET_ELEM:
		el = []
		for word in words:
			el.append(int(word))

		elems.append([el[1], el[2], el[3], el[4]])
			
	i = i + 1	


print("before remving: ", len(xs))
print("before remving: ", len(elems))
new_connectivity = []
xs, ys, zs, elems = RemoveDoublePoints(xs, ys, zs, elems)
#xs, ys, zs, elems = RemoveDoublePoints(xs, ys, zs, elems)
elems = RemoveDoubleElems(elems)

print("after remving: ", len(xs))
print("after remving: ", len(elems))
#print("elems: ", elems)


#print(elems[0])
#print(elems[-1])
#print(xs[0])
#print(len(elems))

nobasepoints = len(xs)
base_elems = copy.deepcopy(elems)

#The base elements (initial layer) is also the layer indicating inlet
inlet = copy.deepcopy(elems)


#Set the radius and the spacing of the first layer 
r = 1.0
delta_r = (1.0005 - 1.0)/2.0


#Normalise the ply mesh to one and recompute for given radius
xs, ys, zs = Normalize(xs, ys, zs)
base_xs = copy.deepcopy(xs)
base_ys = copy.deepcopy(ys)
base_zs = copy.deepcopy(zs)
xs, ys, zs = AdjustRadius(xs, ys, zs, r)

#Add the first layer
all_xs, all_ys, all_zs, all_elems, connectivity = StackFirstLayer(xs, ys, zs, r, delta_r, elems)


n_layers = 64

print("Number of elements:", len(all_elems))
print("Number of vertices:", len(all_xs))
print("Length of connectivity:", len(connectivity))

for l in range(0, n_layers):
	#Increase current radius according to the added layer
	r = r + delta_r

	#Set the spacing of the added layer
	delta_r = ReturnSpacing_idx(l)

        #Increase current radius according to the added layer
        #r = r + delta_r

	#Reassign node coordinates
	xs = copy.deepcopy(all_xs)
	ys = copy.deepcopy(all_ys)
	zs = copy.deepcopy(all_zs)
	connectivity = copy.deepcopy(connectivity)
	elems = copy.deepcopy(all_elems)
	#Add the next layer

	#print("Adding layer at r: ", r)
	all_xs, all_ys, all_zs, all_elems, all_connectivity, added_elems = StackLayer(xs, ys, zs, base_xs, base_ys, base_zs, r, delta_r, elems, base_elems, nobasepoints, 2+l, connectivity)
	print("Number of elements:", len(all_elems))
	print("Number of vertices:", len(all_xs))
	print("Length of connectivity:", len(all_connectivity))
	connectivity = all_connectivity


boundaries = []
inlet_prisms = []
outlet_prisms = []

for i in range(0, len(base_elems)):
	inlet_prisms.append([i, 1])
	out = len(all_connectivity) - len(base_elems) + i
	outlet_prisms.append([out, 2])


boundaries_formatted = inlet_prisms + outlet_prisms

connectivity = all_connectivity

#The following set of paragraphs adjusts the arrays so that they also contain the indices of the vertices and elements
outlet = copy.deepcopy(added_elems)

for b in range(0, len(inlet)):
	inlet[b] = [1] + inlet[b] 
	#new_entry = 
	#for number in range(0, len(inlet[b])):
	#	new_entry.append(number)
for b in range(0, len(outlet)):
        outlet[b] = [2] + outlet[b]

#boundaries_unformatted = inlet + outlet 


#boundaries_formatted = []



#for b in range(0, len(boundaries_unformatted)):
#	elem = boundaries_unformatted[b]
#	new_elem = [b + len(connectivity)]
#	for number in range(0, len(elem)):
#		new_elem.append(elem[number])

#	boundaries_formatted.append(new_elem)

elems_formatted = []

for e in range(0, len(connectivity)):
        elem = connectivity[e]
        new_elem = [e]
        for number in range(0, len(elem)):
                new_elem.append(elem[number])
        elems_formatted.append(new_elem)
       

nodes_formatted = []

for i in range(0, len(all_xs)):
	print all_xs[i], all_ys[i], all_zs[i]

all_xs, all_ys, all_zs = Transform_Rsun(all_xs, all_ys, all_zs)


for n in range(0, len(all_xs)):
        node = [n, all_xs[n], all_ys[n], all_zs[n]]
        nodes_formatted.append(node)


'''
print(connectivity[0])
print(connectivity[len(connectivity)-1])

print(all_xs[0])
print(all_xs[len(xs)])
print(all_ys[0])
print(all_ys[len(xs)])
print(all_zs[0])
print(all_zs[len(xs)])
'''

#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot(all_xs, all_ys, all_zs)
#plt.show()



name = outputfile
path = "/scratch/leuven/338/vsc33811/Mesher/spherical/quad_sphere/"
#name = "sub1_5.brch"

block_type = "prism"
ngrps = 1
nbsets = 2
ndfcd = 3
ndfvl = 3

#print(elems_formatted[0])
written = WriteMesh(path, name, block_type, elems_formatted, nodes_formatted, boundaries_formatted, ngrps, nbsets, ndfcd, ndfvl)

#print("connectivity:", elems_formatted)

print("Written to: ", path, name)

import math
from datetime import datetime
import sys


verynegative = -1e20
verypositive = 1e20
verysmall = 1e-20
verylarge = 1e-20


def add_block(block_type, params):

	if block_type == "2d_rect_quad":
		xmin = params[0]
                xmax = params[1]
                ymin = params[2]
                ymax = params[3]

                refinement = params[4]

		start = (params[5], params[6])

		nodes, elements = make_2d_rect_quad(xmin, xmax, ymin, ymax, refinement, start)

        elif block_type == "3d_box_quad":
                xmin = params[0]
                xmax = params[1]
                ymin = params[2]
                ymax = params[3]
                zmin = params[4]
                zmax = params[5]

                refinement = params[6]

                start = (params[7], params[8])

                nodes, elements = make_3d_box_quad(xmin, xmax, ymin, ymax, zmin, zmax, refinement, start)

     	else:
             	sys.exit("Unknown / unimplemented mesh function. Aborting.")


	return nodes, elements




def delete_repeated_nodes(nodes, elements, tol):

	replace = []
	new_elements = []
	new_nodes = []

	n0 = 0

	all_indices = []
	new_indices = []
        node_map = []

	REMOVED = False
	toremove = 0

	for n1 in range(0, len(nodes)):
		REMOVED = False
		node1 = nodes[n1]
		for n2 in range(0, n1):
			node2 = nodes[n2]

			no_coord = len(node1) - 1
			sim = 0
			for c in range(1, no_coord+1):

				if abs(node1[c] - node2[c]) < tol:
					sim = sim + 1

			if sim == no_coord:
				r = n2
				#replace.append(node2[0], node1[0])
				REMOVED = True
				toremove = toremove + 1
				print "Removing point: ", node1

		if not REMOVED:
			all_indices.append(n1)
			new_indices.append(n1)
			n0 = n0 + 1
		else:
			all_indices.append(r)

		node_map.append(-1)

	# [0, 1, 2, 3, 4, 5, 6, 7, 8] where 2 and 4 are the same and 5 and 7 are the same
	# --> all indices: [0, 1, 2, 3, 2, 5, 6, 5, 8]
	# --> new indices: [0, 1, 2, 3, 5, 6, 8]

	print "New indices:"
	print new_indices
	print "All indices:"
	print all_indices

	#print "toremove:", toremove
	#print "len(all_indices)", len(all_indices)
	#print "len(new_indices):", len(new_indices)
	#print "len(nodes) - toremove", len(nodes) - toremove

	for n in range(0, len(nodes) - toremove):
		original = new_indices[n]
		node = nodes[original]
		node[0] = n
		print "Adding node", original 
		new_nodes.append(node)
		node_map[original] = n

	for e in range(0, len(elements)):
		element = elements[e]
		old_element = [elements[e][0], elements[e][1], elements[e][2], elements[e][3], elements[e][4]]
		no_verts = len(element) - 1

		for v in range(1, no_verts+1):
			vert = element[v]  # say the vertex was number 4 --> vert = 4
			vert_filtered = all_indices[vert] # from new indices --> element[v] = 2
			element[v] = node_map[vert_filtered] # use the node map to find where the node is stored now 
			

		print "Element: ", old_element, " changed to ", element
		new_elements.append(element)

	return new_nodes, new_elements


def get_uniform(index, interval, N):
        I = 1.0 
        zeta = float(index)/float(N-1)

	s = zeta / I
	
	s = s * interval

	return s





def get_negatsin(stretching_factor, index, interval, N):
        I = 1.0


        zeta = float(index)/float(N-1)

        if stretching_factor == 1.:
       	        zeta = float(index)/float(N-1)*(198.)
                s = zeta / I
                s = -0.0213 + 0.0149*zeta - 0.000151*zeta**2 + 0.000000515*zeta**3
                minimum = -0.0213 
                zetamax = 198.
                maximum = -0.0213 + 0.0149*zetamax - 0.000151*zetamax**2 + 0.000000515*zetamax**3
                totalrange = (maximum - minimum)
                s = s - minimum
                s = s / totalrange

        elif stretching_factor == 2.:
                s = -0.0199 + 2.41*zeta - 4.18*zeta**2 + 2.81*zeta**3
                minimum = - 0.0199
                maximum = 1.0201
                totalrange = (-minimum + maximum)
                s = s - minimum
                s = s / totalrange

        else:
                s = 0.00712+1.5*zeta+2.53*zeta**2-16.0*zeta**3+22.7*zeta**4-10.7*zeta**5+0.966*zeta**6
                minimum = 0.00712
                maximum = 1.00312
                totalrange = (-minimum + maximum)
                s = s - minimum
                s = s / totalrange

        #minimum = minimum / totalrange 
        #s = s - minimum
        #s = max(s, 0.0)
        #s = min(s, 1.0)


        s = s * interval

        return s



def get_doubhyptng(stretching_factor, index, interval, N):
	I = 1.0 
	zeta = float(index)/float(N-1)
	delta = stretching_factor

        s = (1.0/2.0 * (1.0 + math.tanh(stretching_factor * (zeta/I - 1.0/2.0)) / math.tanh(stretching_factor/2.0)))

	s = s * interval

	return s


def get_hyptng(stretching_factor, index, interval, N):
        I = interval
        zeta = float(index)/float(N-1)
        delta = stretching_factor

        s = (1.0 + math.tanh(delta*(zeta/I - 1.0))/math.tanh(delta))

	s = s * interval 

	return s



def get_doubhypsin(stretching_factor, index, interval, N):
        I = 1.0 
        zeta = float(index)/float(N-1)
        delta = stretching_factor

        s = (1.0/2.0 * (1.0 + math.sinh(stretching_factor * (zeta/I - 1.0/2.0)) / math.sinh(stretching_factor/2.0)))

        s = s * interval
        
        return s


def get_hypsin(stretching_factor, index, interval, N):
        I = interval
        zeta = float(index)/float(N-1)
        delta = stretching_factor

        s = (1.0 + math.sinh(delta*(zeta/I - 1.0))/math.sinh(delta))

        s = s * interval 

        return s




def make_2d_rect_quad(xmin, xmax, ymin, ymax, refinement, start):
	nodes = []
	elements = []

	origin = [xmin, ymin]

	nx = refinement[0]
        ny = refinement[1]

        refinex = refinement[2]
        refiney = refinement[3]

	stretchingx = refinement[4]
        stretchingy = refinement[5]

	x = origin[0]
	y = origin[1]

	ij = 0

	i_prev = -1
	j_prev = -1

	n_idx = start[0]
	e_idx = start[1]

	e = 0



	for j in range(0, ny):

                if refiney == "uniform":
                        y_00 = get_uniform(j, ymax-ymin, ny)
                elif refiney == "hyptng":
                        y_00 = get_hyptng(stretchingy, j, ymax-ymin, ny)
                elif refiney == "doubhyptng":
                        y_00 = get_doubhyptng(stretchingy, j, ymax-ymin, ny)
                elif refiney == "hypsin":
                        y_00 = get_hypsin(stretchingy, j, ymax-ymin, ny)
                elif refiney == "doubhypsin":
                        y_00 = get_doubhypsin(stretchingy, j, ymax-ymin, ny)
                elif refiney == "negatsin":
                        y_00 = get_negatsin(stretchingy, j, ymax-ymin, ny)
                else:
                        sys.exit("Unknown y mesh function. Aborting.")

                y = origin[1] + y_00

		for i in range(0, nx):
			if refinex == "uniform":
				x_00 = get_uniform(i, xmax-xmin, nx)
			elif refinex == "hyptng":
				x_00 = get_hyptng(stretchingx, i, xmax-xmin, nx)
                        elif refinex == "doubhyptng":
                                x_00 = get_doubhyptng(stretchingx, i, xmax-xmin, nx)
                        elif refinex == "hypsin":
                                x_00 = get_hypsin(stretchingx, i, xmax-xmin, nx)
                        elif refinex == "doubhypsin":
                                x_00 = get_doubhypsin(stretchingx, i, xmax-xmin, nx)
                        elif refinex == "negatsin":
                                x_00 = get_negatsin(stretchingx, i, xmax-xmin, nx)
			else:
				sys.exit("Unknown x mesh function. Aborting.")

			x = origin[0] + x_00

			nodes.append([ij+n_idx, x, y])

			ij = ij + 1

			if (i_prev >= 0 and j_prev >= 0):

				node1 = i_prev 	+ nx * j_prev
				node2 = i 	+ nx * j_prev
				node3 = i_prev 	+ nx * j
				node4 = i 	+ nx * j
                                node1 = node1	+ n_idx 
                                node2 = node2	+ n_idx
                                node3 = node3	+ n_idx
                                node4 = node4	+ n_idx
				elements.append([e+e_idx, node1, node2, node4, node3])

				e = e + 1

                        i_prev = i_prev + 1



		j_prev = j_prev + 1

		i_prev = -1

	return nodes, elements


def make_2d_rect_tri(xmin, xmax, ymin, ymax, refinement):



	return 0


def make_3d_box_quad(xmin, xmax, ymin, ymax, zmin, zmax, refinement, start):
        nodes = []
        elements = []

        origin = [xmin, ymin, zmin]

        nx = refinement[0]
        ny = refinement[1]
	nz = refinement[2]

        refinex = refinement[3]
        refiney = refinement[4]
        refinez = refinement[5]

        stretchingx = refinement[6]
        stretchingy = refinement[7]
        stretchingz = refinement[8]

        x = origin[0]
        y = origin[1]
	z = origin[2]

        ijk = 0

        i_prev = -1
        j_prev = -1
        k_prev = -1

        e = 0

        n_idx = start[0]
        e_idx = start[1]

	for k in range(0, nz):

                if refinez == "uniform":
                        z_000 = get_uniform(k, zmax-zmin, nz)
                elif refinez == "hyptng":
                        z_000 = get_hyptng(stretchingz, k, zmax-zmin, nz)
                elif refinez == "doubhyptng":
                        z_000 = get_doubhyptng(stretchingz, k, zmax-zmin, nz)
                elif refinez == "hypsin":
                        z_000 = get_hypsin(stretchingz, k, zmax-zmin, nz)
                elif refinez == "doubhypsin":
                        z_000 = get_doubhypsin(stretchingz, k, zmax-zmin, nz)
                else:
                        sys.exit("Unknown y mesh function. Aborting.")

                z = origin[2] + z_000


	        for j in range(0, ny):

                        if refiney == "uniform":
                                y_000 = get_uniform(j, ymax-ymin, ny)
                        elif refiney == "hyptng":
                                y_000 = get_hyptng(stretchingy, j, ymax-ymin, ny)
                        elif refiney == "doubhyptng":
                                y_000 = get_doubhyptng(stretchingy, j, ymax-ymin, ny)
                        elif refiney == "hypsin":
                                y_000 = get_hypsin(stretchingy, j, ymax-ymin, ny)
                        elif refiney == "doubhypsin":
                                y_000 = get_doubhypsin(stretchingy, j, ymax-ymin, ny)

                        else:
                                sys.exit("Unknown y mesh function. Aborting.")


                        y = origin[1] + y_000

        	        for i in range(0, nx):
                	        if refinex == "uniform":
                        	        x_000 = get_uniform(i, xmax-xmin, nx)
	                        elif refinex == "hyptng":
        	                        x_000 = get_hyptng(stretchingx, i, xmax-xmin, nx)
                	        elif refinex == "doubhyptng":
	                                x_000 = get_doubhyptng(stretchingx, i, xmax-xmin, nx)
                                elif refinex == "hypsin":
                                        x_000 = get_hypsin(stretchingx, i, xmax-xmin, nx)
                                elif refinex == "doubhypsin":
                                        x_000 = get_doubhypin(stretchingx, i, xmax-xmin, nx)
        	                else:
                	                sys.exit("Unknown x mesh function. Aborting.")

	                        x = origin[0] + x_000

        	                nodes.append([ijk+n_idx, x, y, z])

                	        ijk = ijk + 1

                        	if (i_prev >= 0 and j_prev >= 0 and k_prev >= 0):

                                	node1 = i_prev 	+  nx * j_prev 	+ nx * ny * k_prev
					node2 = i 	+  nx * j_prev 	+ nx * ny * k_prev
                                        node3 = i_prev 	+  nx * j 	+ nx * ny * k_prev
                                        node4 = i 	+  nx * j 	+ nx * ny * k_prev
                                        node5 = i_prev 	+  nx * j_prev 	+ nx * ny * k
                                        node6 = i 	+  nx * j_prev 	+ nx * ny * k
                                        node7 = i_prev 	+  nx * j 	+ nx * ny * k
                                        node8 = i 	+  nx * j 	+ nx * ny * k
           	                    	node1 = node1	+  n_idx
                	                node2 = node2	+  n_idx
                        	        node3 = node3	+  n_idx
                                	node4 = node4	+  n_idx
                                        node5 = node5	+  n_idx
                                        node6 = node6	+  n_idx
                                        node7 = node7	+  n_idx
                                        node8 = node8	+  n_idx

                        	        elements.append([e+e_idx, node1, node2, node3, node4, node5, node6, node7, node8])

                                	e = e + 1

	                        i_prev = i_prev + 1



        	        j_prev = j_prev + 1

                	i_prev = -1



             	k_prev = k_prev + 1

            	i_prev = -1
                j_prev = -1

        return nodes, elements




def make_3d_cyl_quad(xmin, xmax, ymin, ymax, radius, refinement):


        return 0


def make_3d_box_tri(xmin, xmax, ymin, ymax, zmin, zmax, refinement):


        return 0



def make_3d_cyl_tri(xmin, xmax, ymin, ymax, radius, refinement):


        return 0



def detect_2d_rect_boundaries(xmin, xmax, ymin, ymax, nodes, elements, tol):

	boundaries = []

	for e in range(0, len(elements)):

		ele = elements[e]
		n1 = ele[1]
                n2 = ele[2]
                n3 = ele[3]
                n4 = ele[4]

		ns = [n1, n2, n3, n4]

		#print n
		nc1 = nodes[n1]
                nc2 = nodes[n2]
                nc3 = nodes[n3]
                nc4 = nodes[n4]

		ncs = [nc1, nc2, nc3, nc4]
		count = 0

		flags = []

		for n in range(0, 4):
			if abs(ncs[n][1] - xmin) < tol:
                                count = count + 1
				flag = 4
			elif abs(ncs[n][1] - xmax) < tol:
				count = count + 1
				flag = 2

                        elif abs(ncs[n][2] - ymin) < tol:
                                count = count + 1
                                flag = 1
			elif abs(ncs[n][2] - ymax) < tol:
                                count = count + 1
				#print "I AM HERE"
                                flag = 3
			else:
				flag = 0
                                count = count 

			flags.append(flag)



		if count > 0:
			flaglisted = list( dict.fromkeys(flags))
			for f in range(0, len(flaglisted)):
				flag = flaglisted[f]
				if flag > 0:
					boundaries.append([ele[0], flag])


	return boundaries



def detect_3d_rect_boundaries(xmin, xmax, ymin, ymax, zmin, zmax, elements, tol):

        boundaries = []

        for e in range(0, len(elements)):

                ele = elements[e]
                n1 = ele[1]
                n2 = ele[2]
                n3 = ele[3]
                n4 = ele[4]
                n5 = ele[5]
                n6 = ele[6]
                n7 = ele[7]
                n8 = ele[8]

                ns = [n1, n2, n3, n4, n5, n6, n7, n8]

                nc1 = nodes[n1]
                nc2 = nodes[n2]
                nc3 = nodes[n3]
                nc4 = nodes[n4]
                nc5 = nodes[n5]
                nc6 = nodes[n6]
                nc7 = nodes[n7]
                nc8 = nodes[n8]

                ncs = [nc1, nc2, nc3, nc4, nc5, nc6, nc7, nc8]
                count = 0

                flags = []

                for n in range(0, 6):
                        if abs(ncs[n][1] - xmin) < tol:
                                count = count + 1
                                flag = 1
                        elif abs(ncs[n][1] - xmax) < tol:
                                count = count + 1
                                flag = 3

                        elif abs(ncs[n][2] - ymin) < tol:
                                count = count + 1
                                flag = 4
                        elif abs(ncs[n][2] - ymax) < tol:
                                count = count + 1
                                flag = 2

                        elif abs(ncs[n][3] - zmin) < tol:
                                count = count + 1
                                flag = 5   
                        elif abs(ncs[n][3] - zmax) < tol:
                                count = count + 1
                                flag = 6

                        else:
                                flag = 0
                                count = count 

                        flags.append(flag)



                if count > 0:
                        flaglisted = list( dict.fromkeys(flags))
                        for f in range(0, len(flaglisted)):
                                flag = flaglisted[f]
                                if flag > 0:
                                        boundaries.append([ele[0], flag])


        return boundaries



def mesh_get_smallest_size(elements, nodes):


	return 0


def mesh_get_boundaries(nodes, block_type):

	if block_type == "2d_rect_quad":
		xmin = verypositive
		xmax = verynegative
                ymin = verypositive
                ymax = verynegative
                zmin = 0.0
                zmax = 0.0 

		for n in range(0, len(nodes)):
			xmin = min(xmin, nodes[n][1])
			xmax = max(xmax, nodes[n][1])
                        ymin = min(ymin, nodes[n][2])
                        ymax = max(ymax, nodes[n][2])

        elif block_type == "3d_box_quad":
                xmin = verypositive
                xmax = verynegative
                ymin = verypositive
                ymax = verynegative
                zmin = verypositive
                zmax = verynegative

                for n in range(0, len(nodes)):
                        xmin = min(xmin, nodes[n][1])
                        xmax = max(xmax, nodes[n][1])
                        ymin = min(ymin, nodes[n][2])
                        ymax = max(ymax, nodes[n][2])
                        zmin = min(zmin, nodes[n][3])
                        zmax = max(zmax, nodes[n][3])


        else:
          	sys.exit("Boundary detection for the selected block type not yet implemented. Abording.")



	return xmin, xmax, ymin, ymax, zmin, zmax


def write_mesh(path, name, block_type, elements, nodes, boundaries, ngrps, nbsets, ndfcd, ndfvl):
	SUCCESS = 0

	filename = path + name

	f = open(filename, "a")
	line = "        CONTROL INFO 2.4.6" + '\n'
        f.write(line)

	line = "** GAMBIT NEUTRAL FILE" + '\n'
        f.write(line)

	line = "mesh" + '\n'
        f.write(line)

	line = "PROGRAM:                BRCHMESH     VERSION:  0.0.1" + '\n'
        f.write(line)

	now = datetime.now()
 	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	line = dt_string  + '\n'
        f.write(line)

	line = "     NUMNP     NELEM     NGRPS    NBSETS     NDFCD     NDFVL" + '\n'
        f.write(line)
	

	line = str(len(nodes)) + '\n'
        f.write(line)

	line = str(len(elements)) + '\n'
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

	line = "   NODAL COORDINATES 2.4.6" + '\n'
        f.write(line)

	for n in range(0, len(nodes)):
		node = nodes[n]
		if block_type == "2d_rect_quad":
			line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2])  + '\n'

		elif block_type == "3d_box_quad":
                        line = str(node[0]+1) + '\n' + str(node[1]) + '\n' + str(node[2]) + '\n' + str(node[3])  + '\n'


		else:
			sys.exit("Writing for the selected block type not yet implemented. Abording.")

		f.write(line)

	line = "ENDOFSECTION" + '\n'
        f.write(line)
	line = "      ELEMENTS/CELLS 2.4.6"  + '\n'
        f.write(line)

	for e in range(0, len(elements)):
		ele = elements[e]

                if block_type == "2d_rect_quad":
			line = str(ele[0]+1) + '\n' + str(2) + '\n' + str(4) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n'

                elif block_type == "3d_box_quad":
                        line = str(ele[0]+1) + '\n' + str(2) + '\n' + str(4) + '\n' + str(ele[1]+1) + '\n' + str(ele[2]+1) + '\n' + str(ele[3]+1) + '\n' + str(ele[4]+1) + '\n' + str(ele[5]+1) + '\n' + str(ele[6]+1) + '\n' + str(ele[7]+1) + '\n' + str(ele[8]+1) + '\n'

                else:
                        sys.exit("Writing for the selected block type not yet implemented. Abording.")

                f.write(line)


        line = "ENDOFSECTION" + '\n'
        f.write(line)
        line = "       ELEMENT GROUP 2.4.6"  + '\n'
        f.write(line)

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

	if len(line) > 0:
        	f.write(line)

	line = "ENDOFSECTION" + '\n'
        f.write(line)
	line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
        f.write(line)



	
        if block_type == "2d_rect_quad":
		for flag in range(1, 5):

			if flag == 4:
				line = "x0" + '\n'

                        if flag == 2:
                                line = "x1" + '\n'

                        if flag == 1:
                                line = "y0" + '\n'

                        if flag == 3:
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
					line = str(el+1) + "\n" + str(2) + "\n" + str(flag)  + '\n'
				        f.write(line)
	        line = "ENDOFSECTION" + '\n'
        	f.write(line)
        	line = " BOUNDARY CONDITIONS 2.4.6" + '\n'
        	f.write(line)


        elif block_type == "3d_box_quad":
                for flag in range(1, 7):

                        if flag == 1:
                                line = "x0" + '\n'

                        if flag == 3:
                                line = "x1" + '\n'

                        if flag == 2:
                                line = "y0" + '\n'

                        if flag == 4:
                                line = "y1" + '\n'

                        if flag == 5:
                                line = "z0" + '\n'

                        if flag == 6:
                                line = "z1" + '\n'


                        f.write(line)


                        for b in range(0, len(boundaries)):
                                if boundaries[b][1] == flag:
                                        el = boundaries[b][0]
                                        line = str(el+1) + "\n" + str(2) + "\n" + str(flag)  + '\n'
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







def show_element_2d(elements, nodes, which):

	e = elements[which]
	n1 = e[1]
        n2 = e[2]
        n3 = e[3]
        n4 = e[4]

	print "Element: ", which, " has nodes: ", n1, n2, n3, n4 
	print "whith coordinates: ", nodes[n1], nodes[n2], nodes[n3], nodes[n4]

	return 0



def show_element_3d(elements, nodes, which):

        e = elements[which]
        n1 = e[1]
        n2 = e[2]
        n3 = e[3]
        n4 = e[4]
        n5 = e[5]
        n6 = e[6]
        n7 = e[7]
        n8 = e[8]

        print "Element: ", which, " has nodes: ", n1, n2, n3, n4, n5, n6, n7, n8
        print "whith coordinates: ", nodes[n1], nodes[n2], nodes[n3], nodes[n4], nodes[n5], nodes[n6], nodes[n7], nodes[n8]

        return 0






###########################################################################################################################
###########################################################################################################################
###########################################################################################################################


### MAIN PROGRAM GOES HERE



nodes = []
elements = []
boundaries = []
start_n = 0
start_e = 0

# Define and add the first block
xmin = 0.0
xmax = 2.0
ymin = 0.0
ymax = 1.0
tol = 1.e-8

refinement = (250, 250, "negatsin", "hyptng", 3.0, 4.0)
name = "250x250_sin_tg_3_4.brch"
block_type = "2d_rect_quad"
params = [xmin, xmax, ymin, ymax, refinement, start_n, start_e]

nodes_add, elements_add = add_block(block_type, params)
nodes = nodes + nodes_add
elements = elements + elements_add

start_n = len(nodes)
start_e = len(elements)

'''
# Define and add the second block
xmin = 0.8
xmax = 1.2
ymin = 0.0
ymax = 1.0
tol = 1.e-8

refinement = (200, 200, "uniform", "uniform", -2.0, -1.5)

#refinement = (20, 20, "uniform", "doubhyptng", 0.0, 2.5)

block_type = "2d_rect_quad"
params = [xmin, xmax, ymin, ymax, refinement, start_n, start_e]

nodes_add, elements_add = add_block(block_type, params)
nodes = nodes + nodes_add
elements = elements + elements_add


nodes, elements = delete_repeated_nodes(nodes, elements, tol)

# Define and add the third block
xmin = 1.2
xmax = 2.0
ymin = 0.0
ymax = 1.0
tol = 1.e-8

refinement = (150, 200, "uniform", "uniform", -2.0, -1.5)

#refinement = (20, 20, "uniform", "doubhyptng", 0.0, 2.5)

block_type = "2d_rect_quad"
params = [xmin, xmax, ymin, ymax, refinement, start_n, start_e]

nodes_add, elements_add = add_block(block_type, params)
nodes = nodes + nodes_add
elements = elements + elements_add


nodes, elements = delete_repeated_nodes(nodes, elements, tol)



#print "nodes[-1]:", nodes[-1]

#print  show_element_2d(elements, nodes, 0)
'''


#for i in range(0, len(nodes)):
#        print nodes[i][0], nodes[i][1], nodes[i][2]


xmin, xmax, ymin, ymax, zmin, zmax = mesh_get_boundaries(nodes, block_type)


print "These are xmin, xmax, ymin, ymax:"
print xmin, xmax, ymin, ymax

boundaries = detect_2d_rect_boundaries(xmin, xmax, ymin, ymax, nodes, elements, tol)
#print "These are the boundaries:"

#print boundaries

path = "./"
#name = "mesh_sine_150x150.brch"

ngrps = 1
nbsets = 4
ndfcd = 2
ndfvl = 2 
written = write_mesh(path, name, block_type, elements, nodes, boundaries, ngrps, nbsets, ndfcd, ndfvl)





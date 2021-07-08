import sys



def ReadConnectivity(filename):
    connectivity = []
    with open(filename, "r") as ins:
        for line in ins:
            line = line.strip()
            line = line.split()
            x = int(line[0])
            y = int(line[1])
            z = int(line[2])
            
            connectivity.append([x, y, z])

    return connectivity


    
def ReadInviscidData(filename):
    data = []
    nodes = []
    with open(filename, "r") as ins:
        for line in ins:
            line = line.strip()
            line = line.split()
            x = float(line[0])
            y = float(line[1])
            z = float(line[2])
            
            nodes.append([x, y, z])
            data.append(float(line[3]))

    return data, nodes





#BTR_epsilon_nodes.txt  BTR_paths.txt          T_elements.txt         coordinates.txt        mu_nodes.txt           rho_nodes.txt          u_elements.txt         velocities.txt
#BTR_intersections.txt  INFO.txt               T_nodes.txt            dotq_nodes_out.txt     normals.txt            skincf_nodes_out.txt   u_nodes.txt            w_elements.txt
#BTR_nodes_coord.txt    M_elements.txt         centroids.txt          filter.py              p_nodes.txt            stg_point.txt          v_elements.txt         w_nodes.txt
#BTR_nodes_resolved.txt M_nodes.txt            connectivity.txt       mu_elements.txt        rho_elements.txt       theta_nodes_out.txt    v_nodes.txt


connectivity = ReadConnectivity("connectivity.txt")

p, nodes = ReadInviscidData("p_nodes.txt")
qraw, qnodesraw = ReadInviscidData("p_nodes.txt")

q = []
qnodes = []
for i in range(0, len(qnodesraw)):
        if True: #qraw[i] > 100.0 and qraw[i] < 200.0:
                q.append(qraw[i])
                qnodes.append([qnodesraw[i][0], qnodesraw[i][1], qnodesraw[i][2]])

        if True: #qraw[i] > 200.0:
                q.append(180.0)
                qnodes.append([qnodesraw[i][0], qnodesraw[i][1], qnodesraw[i][2]])


values_nodes = []

for i in range(0, len(nodes)):
        value = 0.
        D = 0.
        for j in range(0, len(qnodes)):
                distance = ((nodes[i][0] - qnodes[j][0])**2 + (nodes[i][1] - qnodes[j][1])**2 + (nodes[i][2] - qnodes[j][2])**2 )**0.5
                if distance == 0.:
                        distance = 0.0000001
                value += q[j] * 1./(distance)**1
                D += 1./(distance)**1
        value /= D
        values_nodes.append(value)
        if (i%100 == 0): 
                print "node: ", i, " out of ", len(nodes)


#for i in range(0, len(nodes)):
#        values_nodes.append(1.0)



out = open("tecplot_p.txt", "w")

line = "TITLE = Unstructured grid data \n"
out.write(line)
line = 'VARIABLES =  "x0" "x1" "x2" "q" \n'
out.write(line)                        

E = len(connectivity)
N = len(nodes)

line = 'ZONE   T= "ZONE0 Tri", N=' + str(N) + ', E=' + str(E) + ' , ZONETYPE=FETRIANGLE, DATAPACKING=BLOCK, STRANDID=1, SOLUTIONTIME=0.00000000000000e+00, VARLOCATION=( [1-3]=NODAL,[4]=NODAL)'
out.write(line)                                            


for i in range(0, N):
        line = str(nodes[i][0])+"\n"
        out.write(line)

for i in range(0, N):
        line = str(nodes[i][1])+"\n"
        out.write(line)

for i in range(0, N):
        line = str(nodes[i][2])+"\n"
        out.write(line)

for i in range(0, N):
        line = str(values_nodes[i])+"\n"
        out.write(line)

for c in range(0, E):          
        line = str(connectivity[c][0]+1) + " " + str(connectivity[c][1]+1) + " " + str(connectivity[c][2]+1) + "\n"
	out.write(line)












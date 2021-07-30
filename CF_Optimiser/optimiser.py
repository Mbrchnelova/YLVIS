#Don't touch this
import math
import sys
import time




#Below, set a function yourself --> after how many iterations can we increase the CFL 
#as a function of the current CFL, provided that 90% of the last iterations the residual was decreasing?
def get_CFL_change_iter(CFL):

	#By default, this is set to a 100
	n_iter = 100

	#If we are at CFL of up to 12, then increase CFL after 100 iterations if 90% of them the residual was decreasing
	if CFL < 12:
		n_iter = 100

	#if we are above 12 but below 64, this is 250 iterations and so forth
	elif CFL < 64:
		n_iter = 250
	elif CFL < 512:
		n_iter = 500
	else:
		n_iter = 1000		

	return n_iter





#Below, set a function yourself --> after how many iterations can we decrease the strict coefficient
#provided that we are under the threshold residual? 
def get_coeff_change_iter(coeff):

	#This is by default set to 250, but you can also make this a function of the current coefficient like in case of the CFL
        n_iter = 250

        return n_iter









#####################################################################################################
#Beginning of the programme

#Changing the below will not change much, so feel free
print "\n \n"
print "SIMULATION OPTIMISER"
print "\n \n"

args = str(sys.argv)
if (len(args) > 2):
	print "Keep in mind that this code doesn't take arguments, \nso whatever else you typed in is ignored\n"

#These are default values, they will be overwritten anyway
initial_eps = 1.0
final_eps = 0.0
threshold = -2.0
inter_name = "./quadrupole_1sys.inter"
stop_limiting = True
switchfirstorder= -3.0
pathConvergence = "/scratch/leuven/338/vsc33811/CF_results/CORONA_dipole/convergence.plt-P0.FlowNamespace" 

#This is where the program starts
print "READ CHECK:\n"







#####################################################################################################
#Reading in the settings file



### IMPORTANT TO ADJUST
#All the settings should be in the "script_settings.txt" text file, with the path to this path defined below:
f = open("./script_settings.txt", "r")




lines = f.readlines()
noargs = 0

#Reading in all the settings from the script_settings.txt text file
#Check this section if unsure how to format the script_settings.txt file 
#Everything is also printed on screen for double check
for line in lines:
	if line[0] != "#":
		line_split = line.split("=")
		if line_split[0].strip() == "Intitial_limiter_dissipation_coefficient":
			initial_eps = float((line_split[1]).strip())
			noargs = noargs + 1
			print "Initial epsilon check:", initial_eps, "\n"
		if line_split[0].strip() == "Final_limiter_dissipation_coefficient":
			final_eps = float((line_split[1]).strip())
			noargs = noargs + 1
			print "Final epsilon check:", final_eps, "\n"
		if line_split[0].strip() == "Thershold_residual_for_switching_dissipation_cofficient":
			threshold = float((line_split[1]).strip())
			noargs = noargs + 1
			print "Thershold residual check:", threshold, "\n"
		if line_split[0].strip() == "Stop_limiting_once_down_to_0.0":
			if ((line_split[1]).strip()) == "1":
				stop_limiting = True
				print "Stop limiting option check:",stop_limiting,"\n"
			elif ((line_split[1]).strip()) == "0":
				stop_limiting = False
				print "Stop limiting option check:",stop_limiting, "\n"
			else:
				stop_limiting = False
				print "WARNING: Set the limiting option to either 0 or 1 you cretin.\n"
			noargs = noargs + 1
		if line_split[0].strip() == "Interactive_file_name_and_path":
			inter_name = (line_split[1]).strip()
			noargs = noargs + 1
			print "Interactive file name check:", inter_name, "\n"
		if line_split[0].strip() == "Convergence_file_name_and_path":
			pathConvergence = (line_split[1]).strip()
			noargs = noargs + 1
			print "Convergence path check:", pathConvergence, "\n"
		if line_split[0].strip() == "Switch_order_residual":
			switchfirstorder = (line_split[1]).strip()
			noargs = noargs + 1
			print "Switch to first order residual check:", switchfirstorder, "\n"



#Warn the user if they didn't set something --> then it will be set to a default, probably wrong value
if noargs != 7:
	print("Warning: some script arguments missing! Setting to default values.")

f.close()










#####################################################################################################
#Reading in the residual file and set the basic variables and BOOL



#Open the residual file --> the path defined in the script_settings.txt file above
f  = open(pathConvergence, "r") 
lines = f.readlines()
residuals = []
CFLs = []
iterations = []
cnt = 0

#Read the residuals and load into the corresponding arrays
for line in lines:
	cnt = cnt+1
	#print(line)
	if cnt > 3:
		line_formatted = line.split(" ")

		#Here you have a control over which residual is monitored by the optimiser
		residual = line_formatted[9]


		CFL = line_formatted[11]
		iteration = line_formatted[0]
		residuals.append(float(residual))
		CFLs.append(float(CFL))
		iterations.append(iteration)

f.close()


#Read the current interactive settings
pathInter = inter_name 
f  = open(pathInter, "r")
lines = f.readlines()
line = lines[0]
line_formatted = line.split(" ")
last_change = int(line_formatted[1])
line = lines[2]
line_formatted = line.split(" ")
curr_eps = float(line_formatted[2])
line = lines[5]
line_formatted = line.split(" ")
curr_grad = float(line_formatted[2])
line = lines[6]
line_formatted = line.split(" ")
curr_limstop = int(line_formatted[2])
curr_residual = residuals[-1]
curr_CFL = float(CFLs[-1])
curr_iteration = iterations[-1]
newCFL = curr_CFL
newStrictCoeff = curr_eps
f.close()
since_change = int(curr_iteration) - last_change
initial_cfl = CFLs[0]
prev_eps = curr_eps

#The below info is printed merely to inform the user and check the operation of the optimiser
print("Current residual: ", curr_residual)
print("Current iteration: ", curr_iteration)



#SWITCH_coeff determines whether the dissipation coefficient was just changed --> to set CFL to 1
SWITCH_coeff = False

#SWITCH_CFL determines whether the CFL can be increased yet (enough iterations passed) or not
SWITCH_CFL = True

#SWITCH_TO_SECOND_ORDER makes the code which to gradientFactor 1.0 after a residual determined by switchfirstorder 
SWITCH_TO_SECOND_ORDER = True
SWITCHED_ORDER  = False

#So if this is turned on, we also assume that we start from a first order simulation
order = int(curr_grad)

#if order_change is on, then the order will be increased by 1
order_change = 0

cnt = 0
tot_cnt = 0

#CFL_n_iter --> after how many same-CFL iterations the CFL can change
CFL_n_iter = get_CFL_change_iter(curr_CFL)







#####################################################################################################
#Process the residual data, make modifications


#Determine the value of SWITCH_CFL depending on how many iterations passed since the last change 
#If not enough iterations have passed since the last CFL change, the CFL will not be altered
if len(residuals) > CFL_n_iter+2:
	for i in range(0, CFL_n_iter):
		if curr_CFL == CFLs[-1-i]:
			cnt = cnt + 1
		tot_cnt = tot_cnt + 1

	if tot_cnt == cnt:
		SWITCH_CFL = True
	else:
		SWITCH_CFL = False
else:
	SWITCH_CFL = False	

#Remember - even if SWITCH_CFL is on, this does not mean that the CFL will increase
#CFL will only increase if 90% of the last iterations the residual has been decreasing
#Otherwise, or also if the dissipation level has been changed, then CFL will not increase/ it will go to 1 in case of the latter

#Inform the user whether the CFL can be changed for double checking
print("Switching CFL allowed:", SWITCH_CFL)





#If the simulation is still first order (order = 0) and if we are below switchfirstorder residual, switch to the second order
if float(curr_residual) < float(switchfirstorder) and order == 0 and SWITCH_TO_SECOND_ORDER:
	order = 1
	order_change = curr_iteration
	SWITCHED_ORDER = True #This will later tell the code not to change the limiter values yet
	SWITCH_coeff = True #This will later tell the code to set CFL to 1
	newCFL = 1.0
	print("Second order.")
	last_change = int(curr_iteration)



#Determine how many iterations at the same dissipation coefficient do we need to decrease it
coeff_n_iter = get_coeff_change_iter(curr_eps)



#Determine whether the strict coefficient can decrease and decrease it if applicable (e.g. not if we have just switched order)
if float(curr_residual) < threshold and order == 1:

	#In addition to checking the residual and order, we also want to wait to save the previous solution (here it is assumed that 
	#a solution is saved every 500 iterations)
	#In addition, we also wait until we are enough iterations after the last dissipation change
	#When both conditions are met in addition to the residual and order requirements, we can decrease the dissipation	
	if int(curr_iteration)%500 == 0 and int(since_change) > coeff_n_iter:
		#... obviously if we would not make it a negative value
		if (curr_eps - 0.5) >= 0.0: 

			#Here you are welcome to set a different step, maybe not 0.5, but 0.25 or 0.1, it is up to you
			curr_eps = max(curr_eps - 0.5, 0.0)
			print("Decreasing the strict coefficient to ", curr_eps)
			SWITCH_coeff = True  #This will later tell the code to set CFL to 1
			newCFL = 1.0
			last_change = int(curr_iteration)



#Set the new dissipation coefficient
newStrictCoeff = curr_eps


cnt = 0
tot_cnt = 0





#Now we can go on to handle the CFL

#Count how many last iterations the residual has been decreasing
if len(residuals) > 102 and SWITCH_coeff == False:
	for i in range(0, 100):
		if residuals[-i-1] < residuals[-i-2]:
			cnt = cnt + 1
		tot_cnt = tot_cnt + 1


	#It if was decreasing at least 90% of the 100 iterations, multiply CFL by 2
	#But do this only if we are allowed to switch the CFL, because enough iterations have passed since the last change
	if cnt > 0.9*tot_cnt and SWITCH_CFL: 
		newCFL = float(curr_CFL) * 2.
		print("Increasing the CFL to:", newCFL)

	#Else if it was increasing mostly, either reduce the CFL by 2 (but not below 1)
	if cnt < 0.1*tot_cnt and SWITCH_CFL:
		if float(curr_CFL) / 2.0 > 1.0:
			newCFL = float(curr_CFL) / 2.0
			print("Decreasing the CFL to:", newCFL)

		#or, if that doesn't help and CFL is 1, increase dissipation --> not used for now
		#else:
		#	curr_eps = curr_eps + 0.1
		#	print("Increasing the strict coefficient due to increasing residual to:", curr_eps)
		#	last_change = int(curr_iteration)






#This determines whether the limiting should be turned off (switched from 0 --> 1 in the inter file)
switch_limiting = False


#Finally, if we reached the lowest dissipative setting, turn the limiter off completely if that is desired
if curr_eps == 0.0 and order == 1 and stop_limiting:
	if since_change > coeff_n_iter and int(curr_iteration)%500 == 0:
		switch_limiting = True
		SWITCH_coeff = True
	        newCFL = 1.0
		last_change = int(curr_iteration)
		print("Turned limiting off.")



#However, if the dissipation coefficient change ocurred (change of order, change of diss. coefficient or limiting being turned off), return CFL back to 1
#print("SWITCHED_ORDER", SWITCHED_ORDER)
if SWITCH_coeff or int(since_change) < 100:
	newCFL = 1.0
	print("Adjusting CFL to 1 due to diffusion change.")







#####################################################################################################
#Write the interactive document



#Write the new intrative file with the new info
pathInter = inter_name 
f  = open(pathInter, "w")
line = "#dissipation_change: " + str(last_change) + "\n"
f.write(line)
line = "Simulator.SubSystem.FlowIterator.Data.CFL.Interactive.CFL = " + str(newCFL) + "\n"
f.write(line)
line = "Simulator.SubSystem.Flow.Data.Venktn3DStrict.strictCoeff = " + str(newStrictCoeff) + "\n"
f.write(line)
line = "Simulator.SubSystem.Flow.Data.LinearLS3D.limitRes = -10"  + "\n"
f.write(line)
line = "Simulator.SubSystem.Flow.Data.LinearLS3D.limitIter = 5000"  + "\n"
f.write(line)
line = "Simulator.SubSystem.Flow.Data.LinearLS3D.gradientFactor = " + str(order) + " " + "\n"
f.write(line)
if switch_limiting or curr_limstop == 1:
	line = "Simulator.SubSystem.Flow.Data.LinearLS3D.StopLimiting = 1"  + "\n"
else:
	line = "Simulator.SubSystem.Flow.Data.LinearLS3D.StopLimiting = 0"  + "\n"
f.write(line)
f.close()                                                                       
         

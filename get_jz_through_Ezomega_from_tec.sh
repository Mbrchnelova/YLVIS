#!/bin/bash


mu0=0.000001266
omega=0.116
L0=100000.
B0=0.001 

for f in *.plt ; do

	echo  "#!MC 1410" >>  "${f%.plt}.mcr" >>  "${f%.plt}.mcr"   
	#echo "$""!ReadDataSet  ""\'""\"""/vsc-hard-mounts/leuven-data/338/vsc33811/COOLFluiD_Genius/OPENMPI/optim/plugins/MultiFluidMHD/testcases/MyReconnection/NORADIATION/""$f""\'" >>  "${f%.plt}.mcr"  
	echo "$""!ReadDataSet" '"'"$f"'"' >>  "${f%.plt}.mcr"
	echo "  ReadDataOption = New" >>  "${f%.plt}.mcr"  
	echo "  ResetStyle = No" >>  "${f%.plt}.mcr"  
	echo "  VarLoadMode = ByName" >>  "${f%.plt}.mcr"  
	echo "  AssignStrandIDs = Yes">>  "${f%.plt}.mcr"  
	echo "VarNameList = '"x0" "x1" "Bx" "By" "Bz" "Ex" "Ey" "Ez" "Psi" "Phi" "rho0" "rho1" "U0" "V0" "U1" "V1" "T0" "T1" "emMomX" "emMomy"' " >>  "${f%.plt}.mcr"  

	echo "$""!AlterData" >>  "${f%.plt}.mcr"  
	echo "Equation = '{jz} = {Ez} * 1 / " "$omega" "*" "$mu0" "*" "$L0" "/" "$B0" "'" >>  "${f%.plt}.mcr"

	#echo "$""!ExtendedCommand" >>  "${f%.plt}.mcr"  
	#echo "  CommandProcessorID = 'CFDAnalyzer4'" >>  "${f%.plt}.mcr"  
	#echo "  Command = 'SetFieldVariables ConvectionVarsAreMomentum=\'F\' UVar=3 VVar=4 WVar=5 ID1=\'NotUsed\' Variable1=0 ID2=\'NotUsed\' Variable2=0'"  >>  "${f%.plt}.mcr"  
	#echo "$""!ExtendedCommand " >>  "${f%.plt}.mcr"  
	#echo "  CommandProcessorID = 'CFDAnalyzer4'" >>  "${f%.plt}.mcr"  
	#echo "  Command = 'Calculate Function=\'ZVORTICITY\' Normalization=\'None\' ValueLocation=\'Cellcentered\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''"  >>  "${f%.plt}.mcr"  
	#echo "$"'!WriteDataSet  "/vsc-hard-mounts/leuven-data/338/vsc33811/COOLFluiD_Genius/OPENMPI/optim/plugins/MultiFluidMHD/testcases/MyReconnection/NORADIATION/'"${f%.plt}.dat" >>  "${f%.plt}.mcr"  
	echo "$"'!WriteDataSet "'"${f%.plt}.dat"'"'  >>  "${f%.plt}.mcr"
	echo "  IncludeText = No" >>  "${f%.plt}.mcr"  
	echo "  IncludeGeom = No" >>  "${f%.plt}.mcr"  
	echo "  IncludeCustomLabels = No" >>  "${f%.plt}.mcr"  
	echo "  IncludeDataShareLinkage = Yes" >>  "${f%.plt}.mcr"  
	echo "  VarPositionList =  [21]" >>  "${f%.plt}.mcr"  
	echo "  Binary = No" >>  "${f%.plt}.mcr"  
	echo "  UsePointFormat = No" >>  "${f%.plt}.mcr"  
	echo "  Precision = 9" >>  "${f%.plt}.mcr"  
	echo "  TecplotVersionToWrite = TecplotCurrent" >>  "${f%.plt}.mcr"  


	tec360 -b -p "${f%.plt}.mcr"

done




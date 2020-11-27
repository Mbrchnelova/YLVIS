for f in *.plt ; do


	echo  "#!MC 1410" >>  "${f%.plt}.mcr" 
	echo "$""!ExtendedCommand" >>  "${f%.plt}.mcr"  
	echo "  CommandProcessorID = 'CFDAnalyzer4'" >>  "${f%.plt}.mcr"  
	echo "  Command = 'SetFieldVariables ConvectionVarsAreMomentum=\'F\' UVar=3 VVar=4 WVar=5 ID1=\'NotUsed\' Variable1=0 ID2=\'NotUsed\' Variable2=0'"  >>  "${f%.plt}.mcr"  
	echo "$""!ExtendedCommand " >>  "${f%.plt}.mcr"  
	echo "  CommandProcessorID = 'CFDAnalyzer4'" >>  "${f%.plt}.mcr"  
	echo "  Command = 'Calculate Function=\'ZVORTICITY\' Normalization=\'None\' ValueLocation=\'Nodal\' CalculateOnDemand=\'T\' UseMorePointsForFEGradientCalculations=\'F\''"  >>  "${f%.plt}.mcr"  
	echo "$"'!WriteDataSet  "/vsc-hard-mounts/leuven-data/338/vsc33811/COOLFluiD_Genius/OPENMPI/optim/plugins/MultiFluidMHD/testcases/MyReconnection/NORADIATION/' "${f%.plt}.dat" >>  "${f%.plt}.mcr"  
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




The code is very heavily commented, so just reading through the comments should be enough to be able to understand how it works and adjust it to whatever you would like to do with it.

All the easily modifiable settings are set in the script_settings text file, read by the code. I think the names of the options are self-explanatory, but if not, let me know.

The interactive file will have, in addition to the traditional lines, also a comment line of the top - this one is necessary to be there and the code will write there when the dissipation was changed (otherwise it has no other place where to get this information from). Do not remove it, let the optimiser format it itself. Only once you start again, make sure to set this number back to 0 (and re-set the other numbers obviously, as you always do).

Finally, run this after your CFD iterations started running. If you are going to stay logged in, you can do watch -n 5 python optimiser.py (every 5 seconds, this python script will be ran), otherwise you can run it in the background, with nohup.

If anything doesn't work (as always), is unclear or you wish to modify anything significant, let me know! 

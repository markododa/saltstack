@echo off
set DOMAIN=ADRA
net use * /DELETE /Y >nul 2>&1
echo ## Enter username in format: %DOMAIN%\username  
echo #########################################################
net use L: \\files\Personal /SAVECRED 
net use Z: \\files\Share\zaednicki /SAVECRED 
net use N: \\files\Share\finansii /SAVECRED 
net use P: \\files\Share\point_finansii /SAVECRED 
net use I: \\files\Share\inzenering /SAVECRED 
net use R: \\files\Share\priprema /SAVECRED 
net use X: \\files\Public

echo ## Done!  
pause

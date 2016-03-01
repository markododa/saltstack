@echo off
set DOMAIN=ADRA
echo ## Enter Username: 
set /p UNAME=""

echo ## Disconnecting Shares...
net use L: /DELETE /Y >nul 2>&1
net use Z: /DELETE /Y >nul 2>&1
net use N: /DELETE /Y >nul 2>&1
net use P: /DELETE /Y >nul 2>&1
net use I: /DELETE /Y >nul 2>&1
net use R: /DELETE /Y >nul 2>&1
net use X: /DELETE /Y >nul 2>&1

echo ## Connecting Shares...  
echo ## Enter Password: 


REM Pass credentials once on first mount 

net use L: \\files\Personal /PERSISTENT:NO /USER:%DOMAIN%\%UNAME% * >nul 2>&1
net use Z: \\files\Share\zaednicki /PERSISTENT:NO >nul 2>&1
net use N: \\files\Share\finansii /PERSISTENT:NO >nul 2>&1
net use P: \\files\Share\point_finansii /PERSISTENT:NO >nul 2>&1
net use I: \\files\Share\inzenering /PERSISTENT:NO >nul 2>&1
net use R: \\files\Share\priprema /PERSISTENT:NO >nul 2>&1
net use X: \\files\Public

echo ## Done!  


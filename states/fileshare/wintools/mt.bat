@echo off
set DOM=DOMEJN
echo ## Enter Username: 
set /p UNAME=""

echo ## Disconnecting Shares...
net use P: /DELETE /Y >nul 2>&1
net use S: /DELETE /Y >nul 2>&1
net use X: /DELETE /Y >nul 2>&1

echo ## Connecting Shares...  
echo ## Enter Password: 

REM Pass credentials once on first mount 
REM files is name of the va-fileshare vmachine, replace with IP address

net use P: \\files\Personal /PERSISTENT:NO /USER:%DOM%\%UNAME% * >nul 2>&1
net use S: \\files\Share /PERSISTENT:NO >nul 2>&1
net use X: \\files\Public
echo ## Done!  


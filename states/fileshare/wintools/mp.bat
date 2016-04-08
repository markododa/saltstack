@echo off
set DOM=DOMEJN
net use * /DELETE /Y >nul 2>&1
echo ## Enter username in format: %DOM%\username  
echo #########################################################
REM Replace files with ip of va-fileshare or edit hosts
net use P: \\va-fileshare\Personal /SAVECRED 
net use S: \\va-fileshare\Share\ /SAVECRED 
net use X: \\va-fileshare\Public

echo ## Done!  
pause

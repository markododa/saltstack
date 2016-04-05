@echo off
set DOM=DOMEJN
net use * /DELETE /Y >nul 2>&1
echo ## Enter username in format: %DOM%\username  
echo #########################################################
REM Replace files with ip of va-fileshare or edit hosts
net use P: \\files\Personal /SAVECRED 
net use S: \\files\Share\ /SAVECRED 
net use X: \\files\Public

echo ## Done!  
pause

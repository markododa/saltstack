REM This will disconnect ALL mounted drives
@echo off
echo ## Disconnecting Shares...
net use * /DELETE /Y >nul 2>&1
echo ## Done!  


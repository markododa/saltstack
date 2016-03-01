@echo off
echo ## Disconnecting Shares...
net use L: /DELETE /Y >nul 2>&1
net use Z: /DELETE /Y >nul 2>&1
net use N: /DELETE /Y >nul 2>&1
net use P: /DELETE /Y >nul 2>&1
net use I: /DELETE /Y >nul 2>&1
net use R: /DELETE /Y >nul 2>&1
net use X: /DELETE /Y >nul 2>&1

echo ## Done!  


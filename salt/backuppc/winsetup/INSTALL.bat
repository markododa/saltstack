@echo off
SET mypath=%~dp0
rem echo %mypath:~0,-1%
echo * This script should be in c:\VapourApps and you are in %mypath:~0,-1%

echo * Preparing your Windows machine for BackupPC connectivity.
if not exist "c:\VapourApps\copSSH" mkdir c:\VapourApps\copSSH
if not exist "c:\VapourApps\Backup" mkdir c:\VapourApps\Backup

rem GENERATING RANDOM PASSWORD
setlocal ENABLEEXTENSIONS ENABLEDELAYEDEXPANSION
set alfanum=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789
set pwd=
FOR /L %%b IN (0, 1, 25) DO (
SET /A rnd_num=!RANDOM! * 62 / 32768 + 1
for /F %%c in ('echo %%alfanum:~!rnd_num!^,1%%') do set pwd=!pwd!%%c
)
echo %pwd% > C:\VapourApps\copSSH\pass.txt

echo * Removing previous installation, if exist.

net stop OpenSSHServer

rem ping 127.0.0.1 > nul

net user SvcCOPSSH >nul 2>&1 && net user SvcCOPSSH /delete || echo. 
net user SvcCOPSSH >nul 2>&1 && net user sshd /delete || echo.
if exist "C:\VapourApps\copSSH\uninstall_Copssh.exe" C:\VapourApps\copSSH\uninstall_Copssh.exe /S

ping 127.0.0.1 > nul
rem C:\VapourApps\copSSH\uninstall_ICW_Base /S
if exist "C:\VapourApps\copSSH\uninstall_ICW_OpenSSHServer.exe" C:\VapourApps\copSSH\uninstall_ICW_OpenSSHServer.exe /S

if exist "C:\VapourApps\copSSH\uninstall_ICW_OpenSSHServer.exe" ping 127.0.0.1  > nul

c:\VapourApps\backuppc\Copssh_3.1.3_Installer.exe /u=SvcCOPSSH /p=%pwd% /S /D=C:\VapourApps\copSSH

ping 127.0.0.1 > nul

C:\VapourApps\copSSH\Bin\copsshadm --command activateuser --user SvcCOPSSH --passphrase %pwd%



rem sc query salt-minion | find /i "salt" > NUL && set SALT=Y || set SALT=N
rem if %SALT%==Y echo SALT	: Installed
rem if %SALT%==N echo SALT	: NOT Installed

rem sc query "salt-minion"| find "STATE"| find /v "STOPPED">Nul && set RUN=Y || set RUN=N

rem if %RUN%==Y echo STATE	: Running 
rem if %RUN%==N echo SALT	: NOT Running

rem if %RUN%==N (
rem if %SALT%==Y net start salt-minion
rem )


rem cls
echo * Opening ports on firewall.

rem LOGIC FOR OS CHECK
netsh advfirewall firewall add rule name="OpenSSH" dir=in action=allow protocol=TCP localport=22
rem netsh firewall set portopening protocol = TCP port = 22 name = OpenSSH mode = enable

echo * SSH Server installation finished.
rem c:\VapourApps\cygwin-rsyncd-3.0.9.0_installer
rem echo * RSYNC installation finished.

echo * Restarting SSH Server...
net stop OpenSSHServer
net start OpenSSHServer

rem echo * Stopping RSYNC Server.
rem sc config "RsyncServer" start= disabled
rem sc stop "RsyncServer"

echo * SETUP COMPLETE
echo * User: SvcCOPSSH
echo * Pass: %pwd%
echo * Put SSH key to C:\VapourApps\copSSH\home\SvcCOPSSH\.ssh\authorized_keys


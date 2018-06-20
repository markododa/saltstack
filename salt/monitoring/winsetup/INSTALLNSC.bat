@echo OFF
set MONITORING_IP=192.168.80.44

echo USER	: %username%
echo HOST	: %computername%

reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && set OS=32BIT || set OS=64BIT
if %OS%==32BIT echo OS	: 32bit
if %OS%==64BIT echo OS	: 64bit


sc query nscp | find /i "nscp" > NUL && set SALT=Y || set SALT=N
if %SALT%==Y echo NSCP	: Installed
if %SALT%==N echo NSCP	: NOT Installed


if %SALT%==N (
if %OS%==32BIT msiexec /quiet /passive /i %~dp0NSCP-0.4.4.19-Win32.msi ALLOWED_HOSTS=%MONITORING_IP% INSTALLLOCATION=c:\VapourApps\NSClient ADDDEFAULT=ALL
if %OS%==64BIT msiexec /quiet /passive /i %~dp0NSCP-0.4.4.19-x64.msi ALLOWED_HOSTS=%MONITORING_IP% INSTALLLOCATION=c:\VapourApps\NSClient ADDDEFAULT=ALL
)


ping 127.0.0.1 -n 10 > nul

net stop nscp

rem sc query "nscp"| find "STATE"| find /v "STOPPED">Nul && set RUN=Y || set RUN=N

rem if %RUN%==Y echo STATE	: Running 
rem if %RUN%==N echo STATE	: NOT Running

echo Editing config and reloading...

rem if %RUN%==Y (
rem if %SALT%==Y net stop nscp
rem )

echo [/settings/default] > c:\VapourApps\NSClient\nsclient.ini
echo allowed hosts = %MONITORING_IP% >> c:\VapourApps\NSClient\nsclient.ini
type %~dp0nsclient.txt >> c:\VapourApps\NSClient\nsclient.ini
net start nscp


ping 127.0.0.1 -n 10 > nul
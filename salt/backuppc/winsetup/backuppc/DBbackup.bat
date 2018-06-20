@ECHO OFF
C:\Windows\System32\forfiles.exe /P "c:\VapourApps\Backup" /S /M *.bak /D -30 /C "cmd /c del @PATH" 
sqlcmd -E -S "localhost\SQLEXPRESS" -i c:\VapourApps\backuppc\db_backup_differential.script
echo . | cmd /C date | find /i "Sun" && sqlcmd -E -S "localhost\SQLEXPRESS" -i c:\VapourApps\backuppc\db_backup_full.script
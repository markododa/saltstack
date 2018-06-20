echo %COMPUTERNAME%  %USERNAME% > c:\rsyncd\info.txt
ver >> C:\rsyncd\info.txt
#Uncomment this line and edit appropriately for your site
rem c:\rsyncd\bin\blat.exe c:\rsyncd\info.txt -subject "NEW PC for BackupPC" -to ticket@your.helpdesk.address -server smtp.server.host -f nobody@yourdomain.com

c:\\VapourApps:
  file.directory:
    - makedirs: True

# no acl permission support by minions on win. protection of changes of bat/scripts needed ?
c:\\VapourApps:
  file.recurse:
    - source: salt://backuppc/winsetup
    - makedirs: True

startsetup:
  cmd.run:
    - name: c:\VapourApps\INSTALL.bat

    
# there is now SvcCOPSSH user for SSH with pass at c:\VapourApps\copSSH\pass.txt

# replace C:\VapourApps\copSSH\home\SvcCOPSSH\.ssh\authorized_keys with the key of backuppc

# backuppc shoud accept the fingerprint



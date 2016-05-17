c:\\VapourApps:
  file.directory:
    - makedirs: True

# no acl permission support by minions on win. protection of changes of bat/scripts needed ?
c:\\VapourApps:
  file.recurse:
    - source: salt://monitoring/winsetup
    - makedirs: True

startsetup:
  cmd.run:
    - name: c:\VapourApps\INSTALLNSC.bat

    
# bat contains MONITORING SERVER IP variable. Should be updated first



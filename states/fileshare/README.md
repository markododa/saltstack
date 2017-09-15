# Fileshare


Fileshare acts as normal file server providing Windows file shares. There are three default shares available on the Fileshare application.

\\va-fileshare\Personal - each Directory user have own private folder that can not be shared with others. The network path is same for all users, but the content depends based on the credentails.

\\va-fileshare\Share - is a folder where only valid Directory members can enter. You can create unlimited numbers of subfolders and configure access privileges via folder Properties menu in Explorer.

\\va-fileshare\Public - this one allows unrestricted access to any user without providing credentials. This is useful for sharing files with guest computers or employees that do not need to have own account in Directory.

You can mount/unmount the network shares with these commands:

Remove all existing mapped shares: 

```
net use * /DELETE /Y
```

Map all 3 shares: 

```
net use P: \\va-fileshare\Personal /SAVECRED
net use S: \\va-fileshare\Share\ /SAVECRED
net use X: \\va-fileshare\Public
```

There are also some essential portable administration tools saved in the path \\va-fileshare\Public\Tools\

Access to files and folders and all the actions are logged for security reasons. You can see the current storage usage from "Apps / Fileshare" panel

Recommended folder for back-up is: /home/ (All share folders)
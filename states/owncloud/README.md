# OwnCloud 

OwnCloud is a cloud service for storing and sharing files, calendars, phonebooks. You can use it also as company internal chat platform or webmail client. 
All of the functions are available from the OwnCloud web interface.

It is recommended to use secure HTTPS connection. Permanently accepting the certificate will preventing warnings for self-singed certifiactes.
You can upload and download files, share them with other users or clients. There is an editor/viewer for some common file types. Calendars, tasks and phonebooks can be also edited and shared.

Another way to access ownCloud is with software for Desktop computers or smartphones.
For managing files and syncing we suggest using the offical client.

An alternative for desktop computers is to use the built-in WebDAV support in the operating system. This way you do not keep a local copy of the files, but access is much slower.

On Windows this can be done with:

```
net use Q: \\va-owncloud@SSL\remote.php\webdav /PERSISTENT:YES /user:.USER PASS
```

NOTE: a dot is required before username
On Linux use your default file manager with the "Connect to server..." command. Select server type as "Secure WebDAV"

For calendars/phonebooks a software that support CalDAV and CardDAV is needed. You can use Thunderbird client with these two plugins: Inverse SOGo Connector and Lightning.
For Android you can try "CardDAV" app for the phonebooks and "CalDav Sync Adapter" app for calendar integration. There is also "DAVdroid" that can be both contacts and calendar adapter. 

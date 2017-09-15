# Active Directory

Directory provides features of Microsoft Active Directory. There are 3 sub-sections:
- Users: for managing users (add, remove, enable/disable, change password). You can also autocreate account for VPN services when creating new user. You can do it also from the VPN section later.
- Groups: manage groups (create, remove, change users membership). Most of the built-in groups are hidded for easier work but you can see them on 'View more' button.
- Organizational units (Create or delete OU entries) 
- DNS entries: add DNS entries for new servers (A, AAAA, MX, NS, CNAME) or update existing. SOA entry can not be updated. Be carefull when deleting entries.

Users and groups are used across all other applications, so an user can use single credentails to access all services.

You can also use Remote Server Administratrion Tools (RSAT) from a Windows computer to remotely manage this application. You need to download appropriate version depending on the operating system. After installing the package you need to make them visible by using Taskbar and Start Menu Properties/Customize/System administration tools.

You can use:
- Active Directory Users and Computers
- Group Policy Management
- DNS Manager (connect to server: va-directory)
The Active Directory application is shipped with AD schema version 47 (Windows Server 2008 R2). You can join other Windows Domain Controllers with same schema level (but never use one with a greater schema level)

To join PCs to the domain you need to setup DNS server settings to the IP address of va-directory app 

The best practice is to use this IP address as first DNS servers for all computers. This is neceessary for Windows logging services. It will also make apps available by hostname. 

Recommended folder for back-up is: /var/lib/samba/sysvol/ (Sysvol and Netlogon shares)

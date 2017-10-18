# Backup

The backup application, uses BackupPC for disk-to-disk incremental backup, of all of the VapourApps virtual appliances which are running and can be seen in Apps / Backup / Manage backups. Once VapourApps applications are enabled through the Overview dashboard, predefined backup paths are configured on the Backup application, so no additional configuration is required from the user to perform a daily backup of the configuration and data.

Also through the Manage backups panel, external servers can be added with their paths. It is required for those servers to have salt-minion installed and joined to the salt-master. All servers which are part of the inventory (are joined on the corporate salt-stack) will be listed in the Manage backups panel. After that is configured, adding a backup can be done through the Add backup control, for a particular server.

Once a week, regular full backup is performed on the defined folders and only incremental backup is performed on a daily basis.

The configuration of the backuppc can be found in /etc/backuppc, on the backuppc instance. Direct access to the backuppc web dashboard can be found at: http://%BACKUPPC_HOST%. From there, restoring of the particular files/folders can be performed, in two different ways:

- Direct restore to the location where the backup was initially made;
- Download the desired files as a zip or a tar archive.

More details can be found on the [offical documentation on BackupPC](http://backuppc.sourceforge.net/faq/BackupPC.html)


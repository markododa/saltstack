# Monitoring

The monitoring application uses Icinga2 as the backend monitoring system, in order to monitor the whole infrastructure of your private cloud.

For every host which is running, sensors are added to check different services such as CPU or Disk usage. If the services are green and have status OK, this means that the parameters returned for that particular service are within the normal expected range. If a service returns a check-value outside of the normal expected range, it can have status of Warning or Critical, depending on the severity of the problem.

When an application is enabled, it will be automatically provisioned at the monitoring system. At the moment, adding other hosts and services can also be done, but from the command line, after connecting to the va-monitoring instance (va-monitoring) via ssh. You can get more info from the [latest Icinga2 documentation](http://docs.icinga.org/icinga2/latest/doc/module/icinga2/toc) Adding new hosts and services can be done in the /etc/icinga2/conf.d folder. For upgrade purposes, do not change the existing va_*.cfg files.

If you add additional hosts and services, they will automatically be displayed on the Apps / Monitoring / Status panel of the VapourApps dashboard, together with full performance data graphing.

Installing a standalone monitoring server

To install a standalone monitoring server, download the vapour-apps saltstack repository, then run the masterless.sh script.
The script takes the role of server as an argument, so for monitoring run:

./masterless monitoring

After installing salt for local usage (masterless), set the password for the admin user in /srv/pillar/credentials.sls

Then run salt-call --local state.highstate

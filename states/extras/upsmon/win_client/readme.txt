Run the installer 

Replace the upsmon.conf file with the provided one

Replace the xx.xx.xx.xx with the IP address of the NUT Server where the UPS is connected.

Run the config tool

Disable logging for Info and Debug

Check Install as service and automatic startup

Uncheck Use Timed Shutdown

Use Forced if Hung as shutdown method.

Press Apply and Start WinNUT

The Windows mchine will shutdown at the same time with the NUT server (When battery is critical - 25% battery level).


#!/bin/bash
echo "removing:"
ls /root/backup_* -l | grep '/root'
rm /root/backup_* -rf


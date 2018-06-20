#!/bin/bash
REPO_PATH="/root/saltstack"
PROD_PATH="/srv"
NOW=$(date +"%Y_%m_%d-%H_%M_%S")
NOW="backup_prod_"$NOW
echo Copying from $REPO_PATH to $PROD_PATH: States, Reactors and Modules. 
echo Newer files are not overwritten. Files deleted on source are removed from the destination too.
echo Making copy to /root/$NOW first...
mkdir /root/$NOW
cp $PROD_PATH/* /root/$NOW -R
echo ===============================
echo ==== MODULES AND STATES: ======
rsync -auvrh --progress $REPO_PATH/salt/ $PROD_PATH/salt/

echo ===============================
echo ==== REACTORS: ================
rsync -auvrh --progress $REPO_PATH/reactor/ $PROD_PATH/reactor/

echo ===============================
echo Differences:
/root/saltstack/diffs.sh | grep 'diffs'
echo ===============================
echo Run:
echo salt \'*\' saltutil.sync_all

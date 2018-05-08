#!/bin/bash
REPO_PATH="/root/saltstack"
PROD_PATH="/srv"
NOW=$(date +"%Y_%m_%d-%H_%M_%S")

echo Copying from $REPO_PATH to $PROD_PATH: States, Reactors and Modules. 
echo Newer files are not overwritten. Files deleted on source are removed from the destination too.
echo Making copy to /root/$NOW first...
mkdir /root/$NOW
cp $PROD_PATH/* /root/$NOW -R
mv $PROD_PATH/salt/_modules $PROD_PATH
mv $PROD_PATH/_modules $PROD_PATH/modules
echo ===============================
echo ==== MODULES: =================
rsync -auvrh --progress $REPO_PATH/modules/ $PROD_PATH/modules/

echo ===============================
echo ==== REACTORS: ================
rsync -auvrh --progress $REPO_PATH/reactor/ $PROD_PATH/reactor/

echo ===============================
echo ==== STATES: ==================
rsync -auvrh --progress $REPO_PATH/states/ $PROD_PATH/salt/

mv $PROD_PATH/modules $PROD_PATH/_modules
mv $PROD_PATH/_modules $PROD_PATH/salt/_modules
echo ===============================
echo Differences:
./diffs.sh | grep 'diffs'
echo ===============================
echo Run:
echo salt \'*\' saltutil.sync_all

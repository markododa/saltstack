
#!/bin/bash
REPO_PATH="/root/saltstack"
PROD_PATH="/srv"
NOW=$(date +"%Y_%m_%d-%H_%M_%S")
NOW="backup_repo_"$NOW
echo Copying from $PROD_PATH to $REPO_PATH : States, Reactors and Modules. 
echo Newer files are not overwritten. Files deleted on source are removed from the destination too.
echo Making copy to /root/$NOW first...
mkdir /root/$NOW
cp $REPO_PATH/* /root/$NOW -R
#mv $PROD_PATH/salt/_modules $PROD_PATH
#mv $PROD_PATH/_modules $PROD_PATH/modules

#echo ===============================
#echo ==== MODULES: =================
#rsync --dry-run -auvrh --progress $PROD_PATH/modules $REPO_PATH/modules
#rsync -auvrh --progress $PROD_PATH/modules/ $REPO_PATH/modules/

echo ===============================
echo ==== REACTORS: ================
rsync -auvrh --progress $PROD_PATH/reactor/ $REPO_PATH/reactor/

echo ===============================
echo ==== STATES: ==================
rsync -auvrh --progress $PROD_PATH/salt/ $REPO_PATH/salt/

#mv $PROD_PATH/modules $PROD_PATH/salt
#mv $PROD_PATH/salt/modules $PROD_PATH/salt/_modules
echo ===============================
#echo Run:
#echo salt va-monitoring saltutil.sync_all

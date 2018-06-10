
#!/bin/bash
REPO_PATH="/root/saltstack"
PROD_PATH="/srv"
NOW=$(date +"%Y_%m_%d-%H_%M_%S")

echo Diffs $REPO_PATH and $PROD_PATH: States, Reactors and Modules. 

mv $PROD_PATH/salt/_modules $PROD_PATH
mv $PROD_PATH/_modules $PROD_PATH/modules

echo ===============================
echo ==== MODULES: =================
diff -ENwbur $PROD_PATH/modules $REPO_PATH/modules| grep --color 'diff\|$'

echo ===============================
echo ==== REACTORS: ================
diff -ENwbur $PROD_PATH/reactor $REPO_PATH/reactor | grep --color 'diff\|$'


echo ===============================
echo ==== STATES: ==================
diff -ENwbur $PROD_PATH/states $REPO_PATH/salt | grep --color 'diff\|$'

mv $PROD_PATH/modules $PROD_PATH/salt
mv $PROD_PATH/salt/modules $PROD_PATH/salt/_modules
echo ===============================
echo If you\'re feeling overwhelmed by the results try:
echo "/root/saltstack/diffs.sh | grep '^diff \|^Binary'"

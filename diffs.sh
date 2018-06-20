#!/bin/bash
REPO_PATH="/root/saltstack"
PROD_PATH="/srv"
NOW=$(date +"%Y_%m_%d-%H_%M_%S")

echo Diffs $REPO_PATH and $PROD_PATH: States, Reactors and Modules. 


echo ===============================
echo ==== MODULES AND STATES: ======
diff -ENwbur $REPO_PATH/salt $PROD_PATH/salt | grep --color 'diff\|$'

echo ===============================
echo ==== REACTORS: ================
diff -ENwbur $REPO_PATH/reactor $PROD_PATH/reactor | grep --color 'diff\|$'

echo ===============================
echo If you\'re feeling overwhelmed by the results try:
echo "/root/saltstack/diffs.sh | grep '^diff \|^Binary'"

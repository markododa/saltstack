#!/bin/bash
#git checkout es6_dashboard
service va-master stop
cd /opt/va_master/
rm /opt/va_master/va_dashboard/static/bundle.js -f
find . -type f -name '*.pyc' -delete
git pull
cd va_dashboard/
pwd
rm -rf /opt/va_master/va_dashboard/node_modules
npm i
npm install
node build.js
service va-master start
service va-master status

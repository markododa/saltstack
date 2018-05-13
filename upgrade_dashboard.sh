#!/bin/bash
service va-master stop
cd /opt/va_master/
rm /opt/va_master/va_dashboard/static/bundle.js -f
find . -type f -name '*.pyc' -delete
git pull
cd va_dashboard/
pwd
npm install
node build.js
service va-master start
service va-master status

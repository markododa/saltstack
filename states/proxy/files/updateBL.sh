#!/bin/bash
###
# UpdateBL - refresh DansGuardian Blacklists
#
# Version: 0.9.2-Lince (Juan J. Prieto <jjprieto@eneotecnologia.com>)
# Date: Oct 29 2002
# Author: Fernand Jonker <fernand@futuragts.com>, based largely on 
# the work of Christopher Rath <christopher@rath.ca>
#
# Updated: Sat 27th December 2003 for new provider
#
# A sysadmin named Mike posted the original script to one of the
# ClarkConnect Forums.  It was then rewritten quite extensively by
# Christopher Rath to make it more configurable and to include error
# checking. Thereafter it was customized by Fernand Jonker for 
# use with DansGuardian.
#
# Copy this script to a convenient location and have cron
# periodically run it to keep your blacklists updated.  Please 
# limit automated downloads to twice or ideally once a week to 
# prevent bandwidth wastage. There is also no point in downloading 
# more often as the lists won't change that much.
#
# Ensure you have wget installed on your server - you can obtain
# it from http://www.wget.org/  
#
# Caveat: when UpdateBL moves the new Blacklists into place it
# only replaces Blacklists; that is, if a new Blacklist is not
# downloaded for a particular category then the old list will
# remain in place.  This is a design feature: to allow you to
# have local Blacklists which are never overwritten/refreshed
# by this script.
#
# Info on Dansguardian and Blacklists can be found at:
#     http://dansguardian.org/
#     http://urlblacklist.com/
#    
# No copyright retained.  This script is in the Public Domain.
# This package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  
###

###
# History
#
# 0.9	- Sept 1, 2002 - original release.
# 0.9.1 - Sept 4, 2002 - changed DG restart command and added cron 
#			information - minor cosmetic changes.
# 0.9.2 - Sept 9, 2002 - changed default download to the small test 
#			file and added history
# 0.9.2-Lince - Oct 29 2002 - Now check for update before. Support
#			for LEAF Bering Firewall (busybox)
#
# 0.9.2-Dan - Fri 24th January 2003 - Added comment about commerciality
###

###
# Don't allow undefined variables.
set -u

###
# Settings you must configure.  
#	BL_URL - the Blacklist's URL - test file enabled by default.
#		You must change this to the bigblacklist to download the
#		full blacklist file.
#	B_PATH - where the Blacklist database is stored.
#	SG_UGID - the userid and group which must "own" the Blacklist
#		database files (format: "<userid>:<group>)
#	DG_PATH - where the DansGuardian Binary is located
#	
# 
#export BL_URL=${BL_URL:="http://urlblacklist.com/cgi-bin/commercialdownload.pl?type=download&file=smalltestlist"}
#export BL_URL_INFO=${BL_URL_INFO:="http://urlblacklist.com/cgi-bin/commercialdownload.pl?type=information&file=bigblacklist"}
export BL_URL_INFO=${BL_URL_INFO:="http://download.va.mk/blacklists.info"}
#export BL_URL=${BL_URL:="http://urlblacklist.com/cgi-bin/commercialdownload.pl?type=download&file=bigblacklist"}
export BL_URL=${BL_URL:="http://download.va.mk/blacklists.tar.gz"}

# IMPORTANT - The blacklist is COMMERCIAL.  If you download without a subscription you
#             are stealing.  You may try 1 download of the big list for free to test.
#             For details see: http://urlblacklist.com/

#

export BL_INFO_FILE="/etc/e2guardian/lists/blacklists/blacklists.info"
export DB_PATH=${DB_PATH:="/etc/e2guardian/lists/blacklists"}
export HOME_DIR="/tmp"
export SG_UGID=${SG_UGID:="nobody:nogroup"}
export DG_PATH=${DG_PATH:="/usr/sbin"}
export UNCOMP_CMD="/bin/gunzip"
export UNTAR_DIR="blacklists"
export VERS="0.9.2"

# Create a few working variables.
#export BL_TAR_BASE="`basename ${BL_URL}`"
export BL_TAR_BASE="blacklists.tar.gz"
export BL_TAR_FULL="${HOME_DIR}/${BL_TAR_BASE}"
export TMP_DIR="/tmp/blacklists"
export http_proxy="127.0.0.1:3128"

# We need to check for updates
export BL_URL_INFO=`wget -q -Y on "${BL_URL_INFO}" -O - | head -n 1`
export BL_DATE_NEW=`echo ${BL_URL_INFO} | tr , \\\n  | tr -d \" | head -n 1`
export BL_MD5SUM_NEW=`echo ${BL_URL_INFO} | tr , \\\n  | tr -d \" | grep -v "${BL_DATE_NEW}" | head -n 1`
if [ -e ${BL_INFO_FILE} ]
then
    export BL_DATE=`cat ${BL_INFO_FILE} | grep "DATE:" | sed 's/DATE://'`
    if [ "${BL_DATE}" = "${BL_DATE_NEW}" ]
    then
echo "No new update"
# aborting Blacklist refresh.
	exit 0
    fi
fi

# Starting Blacklist update: 
# We use $TMP_DIR as a working directory for wget and the untar process,
# so we start by cd-ing into it.  We create it if it doesn't exist, and
# if there is already something in the way then we abort.
if [ ! -d "${TMP_DIR}" ]
then
    if [ -e "${TMP_DIR}" ]
    then
        echo "ERROR: ${TMP_DIR} already exists, but isn't a directory;"
        echo "       aborting Blacklist refresh."
        exit 1
    fi
    
    mkdir "${TMP_DIR}"
fi

cd "${TMP_DIR}"
if [ "$?" != "0" ]
then
    echo "ERROR: unable to cd into working directory,"
    echo "       ${TMP_DIR}"
    exit 1
else
    if [ -f "${BL_TAR_FULL}" ]
    then
        rm -f "${BL_TAR_FULL}"
    fi
    
    if [ -f "./${BL_TAR_BASE}" ]
    then
# Removing old ${BL_TAR_BASE}.
        rm -f "./${BL_TAR_BASE}"
    fi
    
# Running wget to retrieve new lists.
echo "downloading..."    
wget -q -Y on "${BL_URL}" -O blacklists.tar.gz
    if [ "$?" != "0" ]
    then
        echo "ERROR: unable to retrieve new lists,"
        echo "       aborting blacklist refresh."
        exit 1
    else
# Succesfully retrieved new lists.

# Uncomment if you have md5sum program installed
	
#	echo "Checking md5sum"
#	export BL_MD5SUM=`md5sum ${BL_TAR_BASE} | tr \  \\\n | head -n 1`
#	if [ "${BL_MD5SUM_NEW}" != "${BL_MD5SUM}" ]
#	    then
#		echo "ERROR: md5sum doesn't match,"
#	        echo "       aborting blacklist refresh."
#		rm -f "./${BL_TAR_BASE}"
#		cd /tmp
#		rm -rf ${TMP_DIR}
#	        exit 1
#	fi

# Untaring Blacklist archive.
        gunzip blacklists.tar.gz
        tar -xf blacklists.tar
        if [ "$?" != "0" ]
        then
            echo "ERROR: unable to extract new lists,"
            echo "       aborting blacklist refresh."
            exit 1
	else
# Moving new lists into place.
            for i in "${UNTAR_DIR}"/*
            do
                export ib="`basename ${i}`"
                if [ -d "${DB_PATH}/${ib}" ]
                then
                    rm -rf "${DB_PATH}/${ib}"
                fi
    
                mv "${UNTAR_DIR}/${ib}" "${DB_PATH}"

            done

# Remove temporary files and folders.
	    cd /tmp
	    rm -rf /tmp/blacklists

# Change owner and permissions.
            chown -R "${SG_UGID}" "${DB_PATH}"
            chmod -R 755 "${DB_PATH}"
	    
# Writting information in blacklists.info and blacklst.version
	    echo "DATE:${BL_DATE_NEW}" > ${BL_INFO_FILE}
	    echo "MD5SUM:${BL_MD5SUM_NEW}" >> ${BL_INFO_FILE}
	    echo "${BL_DATE_NEW}" > /var/lib/lrpkg/blacklst.version
	    chown root:root /var/lib/lrpkg/blacklst.version
	    chmod 644 /var/lib/lrpkg/blacklst.version

# Restarting Dansguardian.

echo "restarting"
	    /etc/init.d/e2guardian restart >/dev/null 2>&1

# Finished Blacklist update.

            exit 0
            ####
echo "OK, done"
            #### If everything went well, we exited here.
            ####
        fi
    fi
fi

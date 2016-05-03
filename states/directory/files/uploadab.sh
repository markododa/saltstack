#! /bin/bash
#
#  VCARD Importer Shell
#  Copyright (c) 2015 Aymeric / APLU <wtf@aplu.fr>
#                All Rights Reserved
#
#  This program is free software. It comes without any warranty, to
#  the extent permitted by applicable law. You can redistribute it
#  and/or modify it under the terms of the Do What the Fuck You Want
#  to Public License, Version 2, as published by Sam Hocevar. See
#  http://www.wtfpl.net/ for more details.


# your user name, if you have a ':' in it, change your login or find an other script as it will not work with this script
user='vlatko.boskoski'
# your password, theoretically any character are allowed, even ':' or '@'
pass='.8Devet-'
# name of the collection
cardsCollection='vcf'
# url of your server, for example with davical
serverURL='http://owncloud.va.mk/remote.php'
# sometimes you may have to edit the following part
serverFullURL=${serverURL}/contactsplus/addressbooks/${user}/${cardsCollection}/

function requirementCheck ()
{
	local fail=0
	# check for grep
	for mendatory in grep sed curl
	do
		type ${mendatory} &>/dev/null
		if [ $? -eq 1 ] 
		then
			echo "Oops, you don't have ${mendatory}, please install it."
			fail=1
		fi
	done
	for opts in csplit uuid
	do
		type ${opts} &>/dev/null
		if [ $? -eq 1 ]
		then
			echo "You don't have ${opts} this is not critical, this script will still work "
		fi
	done
	if [ ${fail} -eq 1 ]
	then
		echo "Error, requirement missing."
		exit 9
	fi
}
function usage ()
{
	echo Usage: $0 Contacts.vcf
	echo Be sure you have correctly changed variable on the begining of $0
	echo Please note, this script will not check against duplicate vCard AND generate a new UID for every vCard.
}

# generate an uuid -v4 using pure bash
function uuidBash ()
{
    local N B C='89ab'

    for (( N=0; N < 16; ++N ))
    do
        B=$(( $RANDOM%256 ))

        case $N in
            6)
                printf '4%x' $(( B%16 ))
                ;;
            8)
                printf '%c%x' ${C:$RANDOM%${#C}:1} $(( B%16 ))
                ;;
            3 | 5 | 7 | 9)
                printf '%02x-' $B
                ;;
            *)
                printf '%02x' $B
                ;;
        esac
    done
}

# generate an uuid v4 using the best method available
function uuidGen ()
{
	# from my own test, uuid is slower than reading /proc witch is slower than the bash method above (mainly due to fork()+exec() calls)
	# for generating 10000 uuid it took:
	# * 12 seconds using uuid
	# * 11 seconds using cat
	# * 4 seconds using bash-function above
	# but I still prefer using uuid
	local lUID
	# generate uuid, if possible using uuid, else we fallback to something else
	type uuid &>/dev/null
	if [ $? -eq 0 ]
	then
		# we found uuid, use it
		lUID=$(uuid -v 4)
	elif [ -f /proc/sys/kernel/random/uuid ]
	then
		# using kernel uuid
		lUID=$(cat /proc/sys/kernel/random/uuid)
	elif [ -f /compat/linux/proc/sys/kernel/random/uuid ]
	then
		# FreeBSD is suppose to have this
		lUID=$(cat /compat/linux/proc/sys/kernel/random/uuid)
	else
		# Fine, you don't want to help, doing it myself
		lUID=$(uuidBash)
	fi
	export UUID=${lUID,,}
}

# slow implementation of csplit for my usecase
function bashsplit ()
{
	# 
	local i=0
	local outfic="xx0000"
	while read line
	do
		if [ -n "${line}" ] && [[ "${line}" =~ "BEGIN:VCARD" ]]
		then
			i=$((i+1))
			outfic=$(printf "xx%05d" ${i})
			echo -n -e "Bash split, VCARD: ${i}\r"
		fi
		echo "${line}" >> $outfic
	done < Contacts.vcf
}

# split a big vcard into smaller file
function vcard_split ()
{
	nbofcards=$(grep -c BEGIN:VCARD "${file}")
	if [ $nbofcards -gt 99999 ] 
	then
		echo "Sorry, this script does not support more than 99999 vcard."
		echo "Counted: $nbofcards"
		exit 8
	fi
	cp -a "${file}" ${tempDir}/Contacts.vcf
	cd ${tempDir}
	# test if we have csplit (as it is from core-utils, it should)
	type csplit &>/dev/null
	if [ $? -eq 0 ]
	then
		# yeah :)
		csplit -s -n 5 -z Contacts.vcf '/BEGIN:VCARD/' '{*}'
	else
		#well… I can also do the same in pure bash, but slower
		bashsplit
	fi
	rm -f Contacts.vcf
}

function fastCardChk ()
{
	local nbBegin nbEnd
	# quick check, does not check against any RFC
	nbBegin=$(grep -c '^BEGIN:VCARD' "${file}")
	nbEnd=$(grep -c '^END:VCARD' "${file}")
	if [ $nbBegin -ne $nbEnd ]
	then
		echo "Error: counted BEGIN:VCARD are not equal to END:VCARD"
		exit 3
	fi
	if [ $nbBegin -eq 0 ]
	then
		echo "Error: VCARD-File?? BEGIN:VCARD not found in file…"
		exit 4
	fi

}

if [ $# -ne 1 ]
then
	usage
	requirementCheck
	exit 1
fi

requirementCheck

file="$1"
if [ ! -f "${file}" ]
then
	echo "ERROR: ${file} not found."
	usage
	exit 2
fi

# first, check VCARD consistent
fastCardChk
# create a tmp dir, so I can work
tempDir=/tmp/contacts.${RANDOM}.d
# if tempDir does not point to /tmp/contacts but / instead, well sorry guys but your bash is buggy
# this rm should never happen, but … in case of 
[ -d ${tempDir} ] && rm -rf ${tempDir}
mkdir -p ${tempDir}
# split the VCARD to files, so we can send them one by one
vcard_split
# now, we are going to push them, one by one to a the remote server
cd ${tempDir}
# build a list of files
find .  -type f -a ! -name 'vcardlist.txt' -fprintf "${tempDir}/vcardlist.txt" "%p\n"

# now for each card, delete any existing UUID, put a new one and rename according the new uuid
while read fic
do
	echo "Working and sending ${fic}"
	#generate an UUID
	#uuidGen
	# remove any ^M, delete any UUID, put the new one generated
	#sed -e "s/\r//" -e '/^UID:.*/d' -e "/^BEGIN:VCARD/a UID:${UUID}" -i ${fic}
	UUID=$(cat ${fic} | grep UID | sed 's/UID://')
	echo $UUID	
# rename the file
	mv ${fic} ${UUID}.vcf
	# send it
	curl --user "${user}:${pass}" --header 'Content-type: text/vcard; charset=UTF-8' -# --anyauth --user-agent 'CARDDAV-Importer/Shell 0.1' -T "${UUID}.vcf" "${serverFullURL}"
done < ${tempDir}/vcardlist.txt

# and cleanup
rm -rf ${tempDir}

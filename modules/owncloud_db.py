import subprocess, re, MySQLdb, hashlib, datetime, time

def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def add_multiple(user, namelist, maillist):
    #Connecting to the database
    db = MySQLdb.connect("localhost","root","","owncloud")
    cursor = db.cursor()
    names = [x for x in namelist]
    mails = [y for y in maillist]
    c = 0
    getid = "SELECT MAX(id) AS id FROM contacts_cards;"
    try:
        cursor.execute(getid)
        theid = cursor.fetchone()
        maxid = theid[0]
    except:
        return "No IDs."
    for name in names:
    	getid = "SELECT id FROM contacts_addressbooks WHERE userid=\""+user+"\";"
	try:
	    cursor.execute(getid)
	    address = cursor.fetchone()
	    addressbookid = address[0]
	except:
	    return "Couldn't get Address Book."
	maxid = maxid + 1
	i = datetime.datetime.now()
	uid = computeMD5hash(mails[i]) #The UID for every contact is their md5hash encoded e-mail
	timestamp = int(time.time())
	#vc = vCard
	vc = "BEGIN:VCARD\nVERSION:3.0\nPRODID:-//ownCloud//NONSGML Contacts 0.5.0.0//EN\nUID:"+str(uid)+"\nN:;"+str(name)+";;;\nFN:"+str(name)+"\nX-MOZILLA-HTML:FALSE\nEMAIL;TYPE=work:"+str(mails[i])+"\nREV:"+i.isoformat()+"\nEND:VCARD\n"
	insertion = "INSERT INTO contacts_cards VALUES ("+str(maxid)+", "+str(addressbookid)+", \'"+str(name)+"\',\'"+vc+"\',\'"+uid+".vcf\' , \'"+str(timestamp)+"\');"
	try:
	    cursor.execute(insertion)
	    db.commit()
	except:
	    db.rollback()
	    return "Couldn't add contact."
	c += 1
    db.close()

def add_contact_for_user(user, email, name = ""):
    #Connectiong to the database
    db = MySQLdb.connect("localhost","root","","owncloud")
    cursor = db.cursor()
# INSERT INTO ~TABELA~ (id, addressbookid, fullname, carddata, uri, lastmodified)
# VALUES (26, 2, ime, vcard, md5sum, timestamp);
	#Number of contacts
    if not name: 
        name = email.replace('@', '.')
    getid = "SELECT MAX(id) AS id FROM contacts_cards;"
    try:
        cursor.execute(getid)
        theid = cursor.fetchone()
        maxid = theid[0]
    except:
        pass
        # print "No IDs."
    #Getting the address book for the user
    getid = "SELECT id FROM contacts_addressbooks WHERE userid=\""+user+"\";"
    try:
        cursor.execute(getid)
        address = cursor.fetchone()
	addressbookid = address[0]
    except:
        # print "Couldn't get Address Book."
        pass
    maxid = maxid + 1
    i = datetime.datetime.now()
    uid = computeMD5hash(email) #The UID for every contact is their md5hash encoded e-mail
    timestamp = int(time.time())
    #vc = vCard
    vc = "BEGIN:VCARD\nVERSION:3.0\nPRODID:-//ownCloud//NONSGML Contacts 0.5.0.0//EN\nUID:"+str(uid)+"\nN:;"+str(name)+";;;\nFN:"+str(name)+"\nX-MOZILLA-HTML:FALSE\nEMAIL;TYPE=work:"+str(email)+"\nREV:"+i.isoformat()+"\nEND:VCARD\n"
    #Adding the contact to the address book
    insertion = "INSERT INTO contacts_cards VALUES ("+str(maxid)+", "+str(addressbookid)+", \'"+str(name)+"\',\'"+vc+"\',\'"+uid+".vcf\' , \'"+str(timestamp)+"\');"
    try:
    	cursor.execute(insertion)
    	db.commit()
    	# print "Success."
    except:
    	# print "Couldn't add contact."
    	db.rollback()
    
    db.close()

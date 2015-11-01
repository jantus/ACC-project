import pickledb
import sys
import os
import swiftclient.client


###############################################################################
# Arguments(1):
#		key: the name of the key 
#		value: a value to the key
# Return:
# 	 
###############################################################################
def to_db(key, value):
	dataBaseName = "pictureDatabase"
	db = pickledb.load(dataBaseName, False)
	dbKeys = db.getall()
	if key not in dbKeys:
		print 1, "Ny grej"
		db.set(key, value)
		db.dump()

###############################################################################
# Arguments(1):
#		fileName: name of the key to search for
# Return:
# 	 	Bool: return True if fileName already exsits 
###############################################################################
def in_db(fileName):
	dataBaseName = "pictureDatabase"
	db = pickledb.load(dataBaseName, False)
	dbKeys = db.getall()
	if fileName in dbKeys:
		return True
	else:
		return False
#!/usr/bin/env python
import vobject

def validateVCF(filename):
	try:
		vfile = open(filename, "r")
		vstring = vfile.read()
		vcard = vobject.readOne(vstring)
	except:
		return False	
	return True

def getPersonName(filename):
	vfile = open(filename, "r")
	vstring = vfile.read()
	vcard = vobject.readOne(vstring)
	return vcard.n.value.given + vcard.n.value.family

if __name__ == "__main__":
	FILENAME1="/var/www/html/contacts/moe.f.khan.vcf"
	FILENAME2="/var/www/cgi-bin/bad.vcf"
	for FILENAME in (FILENAME1, FILENAME2):
		try:
			vfile = open(FILENAME, "r")
			vstring = vfile.read()
			vcard = vobject.readOne(vstring)
			print vcard.prettyPrint()
		except vobject.base.ParseError:
			print FILENAME + " is bad"

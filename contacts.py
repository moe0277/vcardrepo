#!/usr/bin/env python
# vim: expandtab:shiftwidth:ts=4
import os
import cgi
import cvcf
import qrcode
import cgitb; cgitb.enable()

UPLOAD_DIR = "/var/www/html/contacts/"
HEADER = "Content-Type: text/html\n\n"
BASEURL = "http://www.cloudsolutionhubs.com/contacts/"

html1 = """<!DOCTYPE html>
<HTML>
<head>
<meta charset="UTF-8">
<title>VCard Repository</title>
</head>
<body> 

<p>VCard (.vcf) Repo</p>
<hr />
<p>Review Current Records below to see if there is a vcard record for you, if your record is not present,  upload your .vcf file.</p>
<p>The vcard / .vcf file should contain your email address, physical address, and phone number.</p>
<p>Click on your record to get a printable page with a QR code pointing to your .vcf file</p>
<p>You can create a vcard / .vcf file many different ways including via MS Outlook. You can also create it and download from: <a href="http://vcardmaker.com">vcardmaker.com</a>.</p>
<hr />
<p>Upload a valid .vcf file; filename format: <b>firstname.lastname.vcf</b>; for eg: moe.f.khan.vcf</p>
<form name="contacts" method="POST" action="/cgi-bin/contacts.py" enctype="multipart/form-data">
	<input type="file" name="file"></input>
	<input name="submit" type="submit">
</form>
<hr />
<p>Current Records:</p>
<pre>
%s
</pre>
</body>
</HTML>"""

html2="""<HTML>
<head>
<title>CSH Contacts</title>
</head>
<body>
	<h1>Completed file upload</h1>
	<a href="/cgi-bin/contacts.py?person=%s">New Entry</a>
</body>
</form>
</HTML>"""

html3 = """<HTML>
<head>
<title>CSH Contact</title>
</head>
<body> 
<pre>
%s
</pre>
<br />
</body>
</HTML>"""

def getCatalog():
	files = os.listdir(UPLOAD_DIR)
	validfiles = {}
	for filename in files:
		fbase, fext = os.path.splitext(filename)
		if fext == ".vcf":
			if validfiles.has_key(fbase):
				validfiles[fbase] += 1
			else:
				validfiles[fbase] = 1
		elif fext == ".png":
			fbase = fbase.replace(".vcf", "")
			if validfiles.has_key(fbase):
				validfiles[fbase] += 1
			else:
				validfiles[fbase] = 1	
	return validfiles

def getValidFilesHtml(validfiles, uname=None):
	rhtml = "<table>"
	for key, value in validfiles.items():
		if value == 2:
			if ((not uname) or (uname==key)):
				rhtml += "<tr>"
				rhtml += "<td>" + '<img src="%s" height=200 width=200>' % (BASEURL+key + ".vcf.png")   + "</td>"
				rhtml += '<td><a href="/cgi-bin/contacts.py?person=%s">%s</a></td>' % (key, key)
				rhtml += "</tr>"
	rhtml += "</table>"
	return rhtml

def processPerson(person):
	validfiles = getCatalog()
	validfileshtml = getValidFilesHtml(validfiles, person)
	print html3 % validfileshtml

def processFirst():
	validfiles = getCatalog()
	validfileshtml = getValidFilesHtml(validfiles)
	print html1 % validfileshtml

def processFile(ffile, filename):
	f, ext = os.path.splitext(filename)
	if ext != ".vcf":
		print "<h1>Error in filename: %s</h1>" % filename
		print '<a href="/cgi-bin/contacts.py">Back</a>'
	else:
		uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(filename))
		with file(uploaded_file_path, 'wb') as fout:
			while True:
				chunk = ffile.read(100000)
				if not chunk:
					break
				fout.write(chunk)
		fout.close()
		if not cvcf.validateVCF(uploaded_file_path):
			os.remove(uploaded_file_path)
			print "<h1>Invalid format in vcf filename: %s</h1>" % filename
			print '<a href="/cgi-bin/contacts.py">Back</a>'
		else:
			url = BASEURL + filename
			#print '<h1>File URL:%s</h1>' % url
			#print '<h1>%s</h1>' % uploaded_file_path
			img = qrcode.make(url)
			img.save(uploaded_file_path+".png")
			print html2 % filename.replace(".vcf", "")

def process(form):
	if form.has_key('person'):
		processPerson(form['person'].value)
	elif not form.has_key('file'):
		processFirst()
	else:
		form_file = form['file']
		if not form_file.file:
			processFirst()
		elif not form_file.filename:
			processFirst()
		else: 
			processFile(form_file.file, form_file.filename)

		

if __name__ == "__main__":
	print HEADER

	form = cgi.FieldStorage()
	process(form)



import MySQLdb
from werkzeug import secure_filename
from flask import Flask, render_template,request, redirect,flash,url_for,send_from_directory
import os
# Read port selected by the cloud for our application

# Change current directory to avoid exposure of control files


app = Flask(__name__)


# connect
db = MySQLdb.connect(host=" ", 
					user=" ",
					passwd=" ",
					db=" ")

cursor = db.cursor()

# execute SQL select statement
cursor.execute("SELECT * FROM user")

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# get and display one row at a time.


userid = ''
userspace = ''
spacelimit = ''
filelist = []

	
@app.route('/')
@app.route('/index')
def main():
	return render_template('login.html') 
			
			
@app.route('/homepage', methods = ['POST'])
def homepage():
	uname = request.form["uname"]
	password = request.form["password"]
	db = MySQLdb.connect(host=" ", 
					user=" ",
					passwd=" ",
					db=" ")	
	cursor = db.cursor()
	cursor.execute("SELECT * FROM user WHERE uname='"+uname+"' AND password='"+password+"'") 
	db.commit()
	numrows = int(cursor.rowcount)
	
	if numrows > 0:
		for x in range(0,numrows):
			row = cursor.fetchone()
			userid = int(row[0])
			userspace = int(row[3])
			print spacelimit 
		cursor1 = db.cursor()
		cursor1.execute("SELECT *,sum(filesize) as usedspace FROM user_storage WHERE uid = '"+str(userid)+"'")
		db.commit()
		numinrows = int(cursor1.rowcount)
		if numinrows>0:
			for x in range(0,numinrows):
				row = cursor1.fetchone()
				if row[4] == 'NoneType':
					spaceused = int(row[4])
				else:
					spaceused = 0
				
			html=""
			html=html+"<div>Total Space Used:"
			html=html+str(spaceused)+"/"+str(userspace)
			html=html+"</div>"
			
			html=html+"<tr>"
			html=html+"<td>#</td>"
			html=shtml+"<td>FileName\t</td>"
			html=html+"<td>Size\t</td>"
			html=html+"<td>Version\t</td>"
			html=html+"</tr>"	 
			
			for container in range(0,numinrows):
				html=html+"<tr>"
				html=html+"<td><input name='checks' type='checkbox' id='checks' value="+str(row[0])+"\t</td>"
				html=html+"<td>"+str(row[2])+"\t</td>"
				html=html+"<td>"+str(row[3])+"\t</td>"
				html=html+"<td>"+str(row[4])+"\t</td>"
				html=html+"</tr>"
		
		else:
			html = 'There are no file from the user'
		
		html = "<table class='table table-striped'>"+html+"</table>"
		
		db.close
		
		return render_template('form.html',data = html)

		
#route that will process the file upload
@app.route('/uploads', methods = ['POST'])
def uploads():
	print "uploading"
	file = request.files['file']
	filename = secure_filename(file.filename)
	blob = request.files['files'].read()
	size = len(blob)
	print size
	print spaceused
	print spacelimit
	
	if int(size)+int(spaceused) > int(spacelimit):
		
		if file:
			filecontent = file.read
			hashedFileContent= hashlib.md5(str(filecontent)).hexdigest()
				
		db = MySQLdb.connect(host=" ", 
					user=" ",
					passwd=" ",
					db=" ")	
		cursor = db.cursor()
		cursorr.execute("SELECT md5,max(version) as fileversion FROM user_storage WHERE filename = '" + file_name+"'")
		db.commit()
		numrows = int(cursor.rowcount)
		version = ''
		query = ''		
		v=0
		if numrows>0:
			for x in range(0,numrows):
				row = cursor.fetchone()
				oldmd5 = row[0]
				version = row[1]
			
			if oldmd5 == hashedFileContent:
				message = 'Same File already present'
			else:
				try:
					v += version
				except TypeError:
					v=1
				query = "INSERT INTO user_storage VALUES ('','"+str(userid)+"','"+filename+"','"+str(size)+"','','"+str(hashedFileContent)+"','"+str(v)+"')"
		else:
			query = "INSERT INTO user_storage VALUES ('','"+str(userid)+"','"+filename+"','"+str(size)+"','','"+str(hashedFileContent)+"','1')"
		print query
		cursor1 = db.cursor()
		cursor1.execute(query)
		db.commit()
		db.close
		
	return "success"
							   
port = os.getenv('VCAP_APP_PORT','6060')
if __name__ == '__main__':
	app.secret_key = ' '
	app.run(host='127.0.0.1',port=int(port))







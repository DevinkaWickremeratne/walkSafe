from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)

app.secret_key = 'abc123'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'walksafe_db'

# Intialization MySQL
mysql = MySQL(app)


#Definition of routes for the pages of the application
@app.route("/walksafe")
def main():
    return render_template('index.html')

@app.route("/background")
def background():
    return render_template('index.html')

@app.route("/features")
def features():
    return render_template('index.html')

@app.route("/developer")
def developer():
    return render_template('index.html')

#Login Page
@app.route("/login/", methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'guardian_email' in request.form and 'guardian_password' in request.form:
		guardian_email = request.form['guardian_email']
		guardian_password = request.form['guardian_password']

		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM guardian WHERE guardian_email = %s AND guardian_password = %s', (guardian_email, guardian_password))
		guardian1 = cursor.fetchone()

		if guardian1:
			session['loggedin'] = True
			session['guardian_id'] = guardian1['guardian_id']
			session['guardian_email'] = guardian1['guardian_email']
			session['guardian_first_name'] = guardian1['guardian_first_name']
			return redirect(url_for('mainUI'))
		else:
			msg = 'Incorrect email/password!'

	return render_template('login.html', msg=msg)


#Logout Feature
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   # Redirect to login page
   return redirect(url_for('login'))

#Registration Page
@app.route('/register/', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    
    if request.method == 'POST' and 'guardian_first_name' in request.form and 'guardian_last_name' in request.form and 'guardian_email' in request.form and 'guardian_password' in request.form:
        # Create variables for easy access
        guardian_first_name = request.form['guardian_first_name']
        guardian_last_name = request.form['guardian_last_name']
        guardian_email = request.form['guardian_email']
        guardian_password = request.form['guardian_password']
                # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM guardian WHERE guardian_email = %s', [guardian_email])
        guardian2 = cursor.fetchone()
        # If account exists show error and validation checks
        if guardian2:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', guardian_email):
            msg = 'Invalid email address!'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers!'
        elif not guardian_first_name or not guardian_last_name or not guardian_password or not guardian_email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO guardian VALUES (NULL, %s, %s, %s, %s)', (guardian_first_name, guardian_last_name, guardian_email, guardian_password))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # if form is empty
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

#Main user interface for logged in guardian_user
#Currently the UI for a single user is used for convenience
@app.route('/walkSafe/main')
def mainUI():
    # Check if user is loggedin
    if 'loggedin' in session:
        #When guardian is logged in, the main UI will be displayed
        return render_template('mainUI-single.html', guardian_first_name=session['guardian_first_name'])
    # When guardian is not logged in, he will be redirected to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
	app.run()
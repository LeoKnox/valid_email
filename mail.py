import re
from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import MySQLConnection

app = Flask(__name__)
app.secret_key = "make it so number one"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def root():
    return render_template('email.html')

@app.route('/new', methods=['POST'])
def make():
    print(request.form['email'])
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address.")
        return redirect('/')
    elif (len(request.form['email'])<1):
        flash("No email address typed in.")
        return redirect('/')
    else:
        query = "INSERT INTO maillist (email) VALUES (%(e)s);"
        data = {
            'e': request.form['email']
            }
        db = MySQLConnection('mydb')
        insert = db.query_db(query, data)
        print(query)
        flash("Successfully Added")
        return redirect("/list")

@app.route('/list')
def show():
    db = MySQLConnection('mydb')
    query = "SELECT * FROM maillist"
    results = db.query_db(query)
    print(results)

    return render_template('users.html', results=results)

if __name__=='__main__':
    app.run(debug=True)

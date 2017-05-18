from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'groups')
app.secret_key = "pffffffff"


@app.route('/')
def index():
    users = mysql.query_db("SELECT id, CONCAT(first_name, ' ', last_name) AS name, email, DATE_FORMAT(created_at, '%b %D, %Y') AS date FROM users")
    return render_template('index.html', users=users)

# add a new user
@app.route('/users/new')
def add():
    return render_template('add.html')

# process add user
@app.route('/addme', methods=['POST'])
def addme():
    query = "INSERT INTO users (first_name, last_name, email, created_at, updated_at) VALUES(:firstname, :lastname, :email, NOW(), NOW())"
    data = {
        "firstname" : request.form['firstname'],
        "lastname" : request.form['lastname'],
        "email" : request.form['email'],
    }
    mysql.query_db(query, data)
    return redirect('/')

# show particular user
@app.route('/users/<user_id>')
def show(user_id):
    query = "SELECT * FROM users WHERE users.id = :user_id"
    data = { "user_id" : user_id }
    user = mysql.query_db(query, data)
    session['curr_id'] = user_id
    return render_template('user_page.html', user=user[0])

# edit user
@app.route('/users/<user_id>/edit')
def edit(user_id):
    query = "SELECT * FROM users WHERE users.id = :user_id"
    data = { "user_id" : user_id }
    user = mysql.query_db(query, data)
    session['curr_id'] = user_id
    return render_template('edit.html', user=user[0])

# process user edit
@app.route('/process', methods=['POST'])
def update():
    query = "UPDATE users SET first_name = :firstname, last_name = :lastname, email = :email WHERE id = :id"
    data = {
        "firstname" : request.form['firstname'],
        "lastname" : request.form['lastname'],
        "email" : request.form['email'],
        "id" : session['curr_id']
    }
    print request.form['firstname']
    mysql.query_db(query, data)
    return redirect('/')

# delete user
@app.route('/delete/<user_id>')
def delete(user_id):
    query = "DELETE FROM users WHERE id = :id"
    data = {"id": user_id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
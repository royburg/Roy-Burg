from datetime import timedelta
import mysql
from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)

app.secret_key = '123'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)

@app.route('/')
def main():
    return redirect('/home')

@app.route('/home')
def homePage():
    return render_template('home.html')

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

@app.route('/contactUs')
def contactUsPage():
    return redirect(url_for('contactPage'))

@app.route('/Assignment31')
def Assignment3_1():
    hobbies = ('running', 'food', 'books', 'beach', 'parties')
    movies = {
        'Shutter Islands': 138,
        'The Prestige': 130,
        'Inception': 148,
        'The Dark Knight': 152,
        'Interstellar': 169
    }

    return render_template('assignment3_1.html',
                           hobbies=hobbies,
                           movies=movies)

users = {1: {"name": "Roy", "email": "roy@gmail.com"},
         2: {"name": "Messi", "email": "messi@gmail.com"},
         3: {"name": "Ronaldo", "email": "ronaldo@gmail.com"},
         4: {"name": "Neymar", "email": "neymar@gmail.com"},
         5: {"name": "Zlatan", "email": "zlatan@gmail.com"}}


@app.route('/assignment32', methods=['GET', 'POST'])
def Assignment3_2():
    if request.method == 'POST':
        username = request.form['uname_r']
        email = request.form['email_r']
        for user in users:
            if username == users[user]["name"]:
                return render_template('assignment3_2.html',
                                       massage_wrong="User name is already exist, please try other name")

        users.update({list(users.keys())[-1] + 1: {"name": username, "email": email}})
        session['username'] = username
        session['logedin'] = True
        return render_template('assignment3_2.html')

    elif 'uname' in request.args:
        uname = request.args['uname']
        for user in users:
            if users[user]["name"] == uname:
                return render_template('assignment3_2.html',
                                       user_name=users[user]["name"],
                                       user_email=users[user]["email"])

    return render_template('assignment3_2.html',
                           users=users)

@app.route('/log_out')
def log_out():
    session['logedin'] = False
    session.clear()
    return redirect(url_for('Assignment3_2'))

from pages.assignment4.assignment4 import assignment4
app.register_blueprint(assignment4)

if __name__ == '__main__':
    app.run(debug=False)
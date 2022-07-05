import mysql.connector
from flask import Blueprint, render_template, request, redirect, jsonify, url_for
import requests

assignment4 = Blueprint('assignment4', __name__,
                        static_folder='static',
                        template_folder='templates',
                        static_url_path='/assignment4')


@assignment4.route('/assignment4')
def assignment4_func():
    return render_template('assignment4.html')


@assignment4.route('/insert_user', methods=['POST'])
def insert_user():
    name = request.form['name']
    email = request.form['email']
    print(f'{name} {email}')
    query = "INSERT INTO users(name, email) VALUES ('%s', '%s')" % (name, email)
    interact_db(query=query, query_type='commit')
    return render_template('/assignment4.html', message="The changes have been saved!")


@assignment4.route('/delete_user', methods=['POST'])
def delete_user_func():
    user_id = request.form['user_id']
    query = "DELETE FROM users WHERE id='%s';" % user_id
    interact_db(query, query_type='commit')
    return render_template('/assignment4.html', message="The changes have been saved!")


@assignment4.route('/get_users')
def users():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return render_template('assignment4.html', users=users_list)


@assignment4.route('/update_user', methods=['POST'])
def update_user_func():
    user_id = request.form['user_id']
    name = request.form['name']
    email = request.form['email']
    old_name = request.form['old_name']
    old_email = request.form['old_email']
    if name == "":
        name = old_name
    if email == "":
        email = old_email
    query = "UPDATE users SET name = '%s', email = '%s' WHERE id='%s';" % (name, email, user_id)
    interact_db(query, query_type='commit')
    return render_template('assignment4.html', message="The changes have been saved!")


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value


@assignment4.route('/users')
def json_print():
    query = 'select * from users'
    users_list = interact_db(query, query_type='fetch')
    return jsonify(users_list)


@assignment4.route('/outer_source')
def extract_user():
    user_id = request.args.get('backForm_id')
    res = requests.get(f'https://reqres.in/api/users/{user_id}')
    return res.json()

@assignment4.route('/restapi_users')
def user_selection():
    user_id = request.args['restapi_users_form_id']
    if user_id == "":
        return jsonify("[3 ,Roy,roy@gmail.com]")
    return redirect(f'/restapi_users/{user_id}')

@assignment4.route('/restapi_users/<user_id>')
def extract_user_db(user_id):
    query = "SELECT * FROM users"
    users_list = interact_db(query, query_type='fetch')
    for user in users_list:
        if str(user.id) == user_id:
            return jsonify(user)
    return jsonify("Error: There is no user with that ID!")
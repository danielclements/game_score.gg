import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app
import bcrypt

mongo = PyMongo(app)


# Returns the route for the registration page
@app.route('/users/registration', methods=["GET"])
def register_user():
    return render_template('user_registration.html',
                           users=mongo.db.users.find())


# used when a user submits a add user request
# Code was provided by Pretty Printed on youtube
# link in the readme acknowledgments
@app.route('/users/insert', methods=["POST"])
def register():
    users = mongo.db.users
    # checks the username the user just provided agaist the users DB
    existing_user = users.find_one(
        {'username': request.form.get('username')})

    # if the username has not been taken, submit the form to the DB
    if existing_user is None:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt())
        created = datetime.utcnow()
        permission = 'default'
        users.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'username': username,
            'permission': permission,
            'created': created
        })
        session['username'] = request.form.get('username')
        flash(username + ' ' + 'welcome to GameScore.gg!')
        return redirect(url_for('index'))
    # If the username provided already exists
    flash('That Username already exists!')
    return redirect(url_for('register_user'))

# Returns the route for the registration page
@app.route('/users/login', methods=["GET"])
def user_login():
    return render_template('user_login.html')


# used when a user trys to log in
# Code was provided by Pretty Printed on youtube
# link in the readme acknowledgments
@app.route('/users/login/check', methods=["POST"])
def login():
    users = mongo.db.users
    username = request.form.get('username')
    password = request.form.get('password')
    login_user = users.find_one({'username': username})
    # checks if the username and password provided match
    # the data in the DB, if successful user will be logged in
    # and a session will be created
    if login_user:
        if bcrypt.hashpw(password.encode('utf-8'), login_user['password']) == login_user['password']:
            if session:
                session.pop("username")
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    # If user provided details dont match
    flash('Invalid username/password combination')
    return redirect(url_for('user_login'))


# pops the user session and logs them out
@app.route('/users/logout')
def logout():
    session.pop("username")
    flash('You were successfully logged Out')

    return redirect(url_for('home_page'))

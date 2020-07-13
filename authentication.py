import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app
import bcrypt


mongo = PyMongo(app)


@app.route('/users/registration', methods=["GET"])
def register_user():
    return render_template('user_registration.html',
                           users=mongo.db.users.find())


@app.route('/users/insert', methods=["POST"])
def register():
    users = mongo.db.users
    existing_user = users.find_one(
        {'username': request.form.get('username')})

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
    flash('That Username already exists!')
    return redirect(url_for('register_user'))


@app.route('/users/login', methods=["GET"])
def user_login():
    return render_template('user_login.html')


@app.route('/users/login/test', methods=["POST"])
def login():
    users = mongo.db.users
    login_user = users.find_one({'username': request.form.get('username')})

    if login_user:
        if bcrypt.hashpw(request.form.get('password').encode('utf-8'), login_user['password']) == login_user['password']:
            if session:
                session.pop("username")
            session['username'] = request.form['username']
            flash('You were successfully logged in')
            return redirect(url_for('index'))
    flash('Invalid username/password combination')
    return redirect(url_for('user_login'))


@app.route('/users/logout')
def logout():
    session.pop("username")
    flash('You were successfully logged Out')

    return redirect(url_for('home_page'))

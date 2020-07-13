import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


@app.route('/')
def index():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return render_template('home_page.html',
                           games=mongo.db.games.find(),
                           developers=mongo.db.developers.find(),
                           newest_games=mongo.db.games.find().sort("_id", -1).limit(10),
                           newest_developers=mongo.db.developers.find().sort("_id", -1).limit(10),
                           newest_publishers=mongo.db.publishers.find().sort("_id", -1).limit(10))


@ app.route('/adminpanel')
def get_admin_panel():

    if 'username' in session:
        if session["username"] == 'admin':
            return render_template('adminpanel.html',
                                   categories=mongo.db.categories.find(),
                                   games=mongo.db.games.find(),
                                   publishers=mongo.db.publishers.find(),
                                   developers=mongo.db.developers.find(),
                                   platforms=mongo.db.platforms.find(),
                                   reviews=mongo.db.reviews.find())
        else:
            flash("Please Log In as Administrator to access this page")
            return redirect(url_for('user_login'))
    else:
        flash("Please Log In as Administrator to access this page")
        return redirect(url_for('user_login'))

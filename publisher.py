import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


# Create Publisher
@ app.route('/publisher/add')
def add_publisher():
    if 'username' in session:
        return render_template('add_publisher.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_publisher', methods=['POST'])
def insert_publisher():
    publishers = mongo.db.publishers
    publisher_name = request.form.get('publisher_name')
    publisher_desc = request.form.get('publisher_desc')
    publisher_founding_date = request.form.get('publisher_founding_date')
    added_by = session['username']
    date_added = datetime.utcnow()
    publishers.insert_one({
        'publisher_name': publisher_name,
        'publisher_desc': publisher_desc,
        'publisher_founding_date': publisher_founding_date,
        'added_by': added_by,
        'date_added': date_added

    })
    flash(publisher_name + ' ' + "successfully added")
    return redirect(url_for('view_publishers'))


# View Publishers
@ app.route('/publishers')
def view_publishers():
    return render_template('view_publishers.html',
                           publishers=mongo.db.publishers.find())


@app.route('/publishers/<publisher_name>')
def view_publisher_games(publisher_name):
    the_pub = mongo.db.publishers.find_one({"publisher_name": publisher_name})
    all_games = mongo.db.games.find({'publisher_name': publisher_name})
    return render_template('view_publisher_details.html',
                           games=all_games,
                           the_publisher=the_pub,
                           )


# Update Publisher
@ app.route('/publisher/edit/<publisher_id>')
def edit_publisher(publisher_id):
    the_publisher = mongo.db.publishers.find_one(
        {'_id': ObjectId(publisher_id)})
    creator = the_publisher['added_by']
    if 'username' in session:
        if session['username'] == creator:
            return render_template('edit_publisher.html',
                                   publisher=the_publisher)
        else:
            flash('Please login as  ' + creator)
            return redirect(url_for('user_login'))
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/update_publisher/<publisher_id>', methods=['POST'])
def update_publisher(publisher_id):
    publishers = mongo.db.publishers
    publishers.update_one({'_id': ObjectId(publisher_id)},
                          {
        '$set': {
            'publisher_name': request.form.get('publisher_name'),
            'publisher_desc': request.form.get('publisher_desc'),
            'publisher_founding_date': request.form.get('publisher_founding_date'),
            'edit_date': datetime.utcnow()

        }})
    return redirect(url_for('get_admin_panel'))

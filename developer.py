import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


# Create Developer
@app.route('/developer/add')
def add_developer():
    if 'username' in session:
        return render_template('add_developer.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_developer', methods=['POST'])
def insert_developer():
    developers = mongo.db.developers
    developer_name = request.form.get('developer_name')
    developer_desc = request.form.get('developer_desc')
    developer_founding_date = request.form.get('developer_founding_date')
    added_by = session['username']
    date_added = datetime.utcnow()
    developers.insert_one({
        'developer_name': developer_name,
        'developer_desc': developer_desc,
        'developer_founding_date': developer_founding_date,
        'added_by': added_by,
        'date_added': date_added
    })
    flash(developer_name + ' ' + "successfully added")
    return redirect(url_for('view_developers'))


# Update Developer
@ app.route('/developer/edit//<developer_id>')
def edit_developer(developer_id):
    the_developer = mongo.db.developers.find_one(
        {'_id': ObjectId(developer_id)})
    creator = the_developer['added_by']
    if 'username' in session:
        if session['username'] == creator:
            return render_template('edit_developer.html',
                                   developer=the_developer)
        else:
            flash('Please login as :  ' + creator)
            return redirect(url_for('user_login'))
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/edit_developer/<developer_id>', methods=['POST'])
def update_developer(developer_id):
    developers = mongo.db.developers
    developers.update_one({'_id': ObjectId(developer_id)},
                          {
                          '$set': {
                              'developer_name': request.form.get('developer_name'),
                              'developer_desc': request.form.get('developer_desc'),
                              'developer_founding_date': request.form.get('developer_founding_date'),
                              'edit_date':  datetime.utcnow()
                          }})
    return redirect(url_for('get_admin_panel'))


# View Developers
@app.route('/developers')
def view_developers():
    return render_template('view_developers.html',
                           developers=mongo.db.developers.find())


@app.route('/developers/<developer_name>')
def view_developer_games(developer_name):
    the_dev = mongo.db.developers.find_one({"developer_name": developer_name})
    all_games = mongo.db.games.find({'developer_name': developer_name})
    return render_template('view_developer_details.html',
                           games=all_games,
                           the_dev=the_dev,
                           )

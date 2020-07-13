import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


# Create Category
@ app.route('/category/add')
def add_category():
    if 'username' in session:
        return render_template('add_category.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_category', methods=['POST'])
def insert_category():
    category_name = request.form.get('category_name')
    category_doc = {'category_name': category_name,
                    'added_by': session['username']}
    mongo.db.categories.insert_one(category_doc)
    flash('Category: ' + category_name + ' successfully added!')
    return redirect(url_for('home_page'))


# Update Category
@ app.route('/category/edit/<category_id>')
def edit_category(category_id):
    the_category = mongo.db.categories.find_one(
        {'_id': ObjectId(category_id)})
    creator = the_category['added_by']
    if 'username' in session:
        if session['username'] == creator:
            return render_template('edit_category.html',
                                   category=the_category)
        else:
            flash('Please log in as   ' + creator)
            return redirect(url_for('user_login'))
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/edit_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update_one({'_id': ObjectId(category_id)},
                                   {
        '$set': {
            'category_name': request.form.get('category_name'),
            'edit_date': datetime.utcnow()}})
    return redirect(url_for('get_admin_panel'))

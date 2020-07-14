import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


# Create Review
@ app.route('/review/add')
def add_review():
    if 'username' in session:
        return render_template('add_review.html',
                               games=mongo.db.games.find())
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@app.route('/insert_review', methods=['POST'])
def insert_review():
    users = mongo.db.users
    login_user = users.find_one({'username': session['username']})
    reviews = mongo.db.reviews
    review_game = request.form.get('review_game')
    review_header = request.form['review_header']
    review_author = login_user['first_name'] + ' ' + login_user['last_name']
    review_body = request.form['review_body']
    review_date = datetime.utcnow()
    review_score = int(request.form['review_score'])
    review_by = login_user['username']
    reviews.insert_one({
        'review_game': review_game,
        'review_header': review_header,
        'review_author': review_author,
        'review_body': review_body,
        'review_date': review_date,
        'review_score': review_score,
        'review_by': review_by
    })
    flash('Your review of ' + review_game + ' was successfully added!')
    return redirect(url_for('home_page'))


# Add review by game
@app.route('/review/game/<game_id>')
def review_by_game(game_id):
    the_game = mongo.db.games.find_one({'_id': ObjectId(game_id)})
    print(the_game)
    if 'username' in session:
        return render_template('add_review.html',
                               the_game=the_game,
                               games=mongo.db.games.find())
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


# Read Reviews
@ app.route('/games/review/<game_id>')
def view_game_review(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_reviews = mongo.db.reviews.find()
    return render_template('view_game_review.html',
                           reviews=all_reviews,
                           game=the_game,
                           )


# Update Review
@ app.route('/review/edit/<review_id>', methods=['get'])
def edit_review(review_id):
    the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    creator = the_review['review_by']
    all_games = mongo.db.games.find()
    print(creator)
    if 'username' in session:
        if session['username'] == creator:
            return render_template('edit_review.html',
                                review=the_review,
                                games=all_games)
        else:
            flash('please login as:' + creator)
            return redirect(url_for('user_login'))
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/update_review/<review_id>', methods=['POST'])
def update_review(review_id):
    the_review = mongo.db.review.find_one({'_id': ObjectId(review_id)})
    print(the_review)
    reviews = mongo.db.reviews
    review_game = request.form.get('review_game')
    reviews.update_one({'_id': ObjectId(review_id)},
                       {
        '$set': {
            'review_game': review_game,
            'review_header': request.form.get('review_header'),
            'review_body': request.form.get('review_body'),
            'review_edit_date': datetime.utcnow(),
            'review_score': int(request.form.get('review_score'))
        }})
    flash('Your review of ' + review_game + ' was successfully updated')
    return redirect(url_for('home_page'))


# Delete Review
@app.route('/review/delete<review_id>')
def delete_review(review_id):
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    flash('Successfully deleted review!')
    return redirect(url_for('home_page'))

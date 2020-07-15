import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
from app import app

mongo = PyMongo(app)


# Create Games
@ app.route('/games/add')
def add_game():
    if 'username' in session:
        return render_template('add_game.html',
                               categories=mongo.db.categories.find(),
                               developers=mongo.db.developers.find(),
                               publishers=mongo.db.publishers.find(),
                               platforms=mongo.db.platforms.find())
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@app.route('/insert_game', methods=['POST'])
def insert_game():
    games = mongo.db.games
    platforms = request.values.getlist('platforms')
    game_categories = request.values.getlist('game_categories')
    game_name = request.form['game_name']
    game_summ = request.form['game_summ']
    developer_name = request.form.get('developer_name')
    publisher_name = request.form.get('publisher_name')
    release_date = request.form['release_date']
    game_image_url = request.form['game_image_url']
    game_added_by = session['username']
    game_add_date = datetime.utcnow()

    games.insert_one({
        'game_name': game_name,
        'game_categories': game_categories,
        'platforms': platforms,
        'game_summ': game_summ,
        'developer_name': developer_name,
        'publisher_name': publisher_name,
        'release_date': release_date,
        'game_image_url': game_image_url,
        'game_added_by': game_added_by,
        'game_add_date': game_add_date
    })
    flash(game_name + ' ' + 'successfully added!')
    return redirect(url_for('view_games'))


# Read Games
@ app.route('/games')
def view_games():
    return render_template('view_games.html',
                           games=mongo.db.games.find(),
                           categories=mongo.db.categories.find())


@ app.route('/games/category/<category_name>')
def view_games_by_category(category_name):
    return render_template('view_games.html',
                           games=mongo.db.games.find({"game_categories":
                                                      category_name}),
                           categories=mongo.db.categories.find())


# Update Games
@app.route('/game/edit/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    creator = the_game['game_added_by']
    if 'username' in session:
        if session['username'] == creator:
            return render_template('edit_game.html', game=the_game,
                                   games=mongo.db.games.find(),
                                   categories=mongo.db.categories.find(),
                                   developers=mongo.db.developers.find(),
                                   publishers=mongo.db.publishers.find(),
                                   platforms=mongo.db.platforms.find(),)
        else:
            flash('Please log in as: ' + creator)
            return redirect(url_for('user_login'))

    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    games = mongo.db.games
    game_name = request.form.get('game_name')
    games.update_one({'_id': ObjectId(game_id)},
                     {
                     '$set': {
                         'game_name': game_name,
                         'game_categories': request.form.getlist('game_categories'),
                         'platforms': request.values.getlist('platforms'),
                         'developer_name': request.form.get('developer_name'),
                         'publisher_name': request.form.get('publisher_name'),
                         'release_date': request.form.get('release_date'),
                         'game_summ': request.form.get('game_summ'),
                         'game_image_url': request.form['game_image_url'],
                         'game_edit_date': datetime.utcnow()
                     }})
    flash(game_name + " " + "successfully edited!")
    return redirect(url_for('view_games'))


# Delete Review
@app.route('/games/delete<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    flash('Successfully deleted game!')
    return redirect(url_for('home_page'))

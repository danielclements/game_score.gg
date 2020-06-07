import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


if path.exists('env.py'):
    import env

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "Game_Score"
COLLECTION_NAME = "Games"

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Game_score'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')


@app.route('/add_game')
def add_game():
    return render_template('addgame.html', categories=mongo.db.categories.find(), developers=mongo.db.developers.find(), publishers=mongo.db.publishers.find(), platforms=mongo.db.platforms.find())


mongo = PyMongo(app)


@app.route('/insert_game', methods=['GET', 'POST'])
def insert_game():
    games = mongo.db.Games
    platforms = request.values.getlist('platforms')
    category_name = request.values.getlist['category_name']
    game_name = request.form['game_name']
 
    games.insert_one({
                        'game_name': game_name,
                        'category_name': category_name,
                        'platforms': platforms
                    })

    return redirect(url_for('add_game'))


@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())









if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
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
    return render_template('addgame.html', categories=mongo.db.categories.find(),
                                           developers=mongo.db.developers.find(), 
                                           publishers=mongo.db.publishers.find(), 
                                           platforms=mongo.db.platforms.find())


mongo = PyMongo(app)


@app.route('/insert_game', methods=['GET', 'POST'])
def insert_game():
    games = mongo.db.Games
    platforms = request.values.getlist('platforms')
    categories = request.values.getlist('categories')
    game_name = request.form['game_name']
    developer_name = request.values.getlist('developer_name')
    publisher_name = request.values.getlist('publisher_name')
    release_date = request.form['release_date']
    affiliate_link = request.form['affiliate_link']
    games.insert_one({
                        'game_name': game_name,
                        'categories': categories,
                        'platforms': platforms,
                        'developer_name': developer_name,
                        'publisher_name': publisher_name,
                        'release_date': release_date,
                        'affiliate_link': affiliate_link
                    })

    return redirect(url_for('add_game'))

@app.route('/')
@app.route('/get_admin_panel')
def get_admin_panel():
    return render_template('adminpanel.html',
                            categories=mongo.db.categories.find(),
                            games=mongo.db.Games.find(),
                            publishers=mongo.db.publishers.find(),
                            developers=mongo.db.developers.find(),
                            platforms=mongo.db.platforms.find())


@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.Games.find_one({"_id": ObjectId(game_id)})
    return render_template('editgame.html', game=the_game,
                                            categories=mongo.db.categories.find(),
                                            developers=mongo.db.developers.find(), 
                                            publishers=mongo.db.publishers.find(), 
                                            platforms=mongo.db.platforms.find())


@app.route('/update_game/<game_id>', methods=["POST", "GET"])
def update_game(game_id):
    games = mongo.db.Games
    games.update({'_id': ObjectId(game_id)},
    {
        'game_name': request.form.get('game_name'),
        'categories': request.form.get('categories'),
        'platforms': request.values.getlist('platforms'),
        'developer_name': request.values.getlist('developer_name'),
        'publisher_name': request.values.getlist('publisher_name'),
        'release_date': request.form.get('release_date'),
        'affiliate_link': request.form.get('affiliate_link')
    })

    return redirect(url_for('get_admin_panel'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


@app.route('/insert_category', methods=['POST', 'GET'])
def insert_category():
        category_doc = {'category_name': request.form.get('category_name')}
        mongo.db.categories.insert_one(category_doc)
        return redirect(url_for('get_admin_panel'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
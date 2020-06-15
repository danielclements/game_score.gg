import os
from os import path
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


if path.exists('env.py'):
    import env

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "Game_Score"
COLLECTION_NAME = "games"

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'Game_score'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)

# Initial load page


@app.route('/')
@app.route('/get_admin_panel')
def get_admin_panel():
    return render_template('adminpanel.html',
                           categories=mongo.db.categories.find(),
                           games=mongo.db.games.find(),
                           publishers=mongo.db.publishers.find(),
                           developers=mongo.db.developers.find(),
                           platforms=mongo.db.platforms.find())

# Routing and functions to add to the database


@app.route('/add_game')
def add_game():
    return render_template('addgame.html', categories=mongo.db.categories.find(),
                           developers=mongo.db.developers.find(),
                           publishers=mongo.db.publishers.find(),
                           platforms=mongo.db.platforms.find())


@app.route('/insert_game', methods=['GET', 'POST'])
def insert_game():
    games = mongo.db.games
    platforms = request.values.getlist('platforms')
    categories = request.values.getlist('categories')
    game_name = request.form['game_name']
    game_summ = request.form['game_summ']
    developer_name = request.values.getlist('developer_name')
    publisher_name = request.values.getlist('publisher_name')
    release_date = request.form['release_date']
    affiliate_link = request.form['affiliate_link']
    games.insert_one({
        'game_name': game_name,
        'categories': categories,
        'platforms': platforms,
        'game_summ': game_summ,
        'developer_name': developer_name,
        'publisher_name': publisher_name,
        'release_date': release_date,
        'affiliate_link': affiliate_link
    })

    return redirect(url_for('get_admin_panel'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')


@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_admin_panel'))


@app.route('/add_publisher')
def add_publisher():
    return render_template('add_publisher.html')


@app.route('/insert_publisher', methods=['GET', 'POST'])
def insert_publisher():
    publishers = mongo.db.publishers
    publisher_name = request.form.get('publisher_name')
    publisher_desc = request.form.get('publisher_desc')
    publisher_founding_date = request.form.get('publisher_founding_date')
    publishers.insert_one({
        'publisher_name': publisher_name,
        'publisher_desc': publisher_desc,
        'publisher_founding_date': publisher_founding_date

    })
    return redirect(url_for('get_admin_panel'))


@app.route('/add_review')
def add_review():
    return render_template('add_review.html',
                           games=mongo.db.games.find())


@app.route('/insert_review', methods=['POST', 'GET'])
def insert_review():
    reviews = mongo.db.reviews
    review_game = request.form.get('review_game')
    review_header = request.form['review_header']
    review_author = request.form['review_author']
    review_body = request.form['review_body']
    review_date = request.form['review_date']
    review_score = request.form['review_score']

    reviews.insert_one({
        'review_game': review_game,
        'review_header': review_header,
        'review_author': review_author,
        'review_body': review_body,
        'review_date': review_date,
        'review_score': review_score,
    })

    return redirect(url_for('get_admin_panel'))


@app.route('/add_developer')
def add_developer():
    return render_template('add_developer.html')


@app.route('/insert_developer', methods=['GET', 'POST'])
def insert_developer():
    developers = mongo.db.developers
    developer_name = request.form.get('developer_name')
    developer_desc = request.form.get('developer_desc')
    developer_founding_date = request.form.get('developer_founding_date')
    developers.insert_one({
        'developer_name': developer_name,
        'developer_desc': developer_desc,
        'developer_founding_date': developer_founding_date
    })
    return redirect(url_for('get_admin_panel'))


# Edit database sectionå


@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template('editgame.html', game=the_game,
                           categories=mongo.db.categories.find(),
                           developers=mongo.db.developers.find(),
                           publishers=mongo.db.publishers.find(),
                           platforms=mongo.db.platforms.find())


@app.route('/update_game/<game_id>', methods=["POST", "GET"])
def update_game(game_id):
    games = mongo.db.games
    games.update({'_id': ObjectId(game_id)},
                 {
        'game_name': request.form.get('game_name'),
        'categories': request.form.getlist('categories'),
        'platforms': request.values.getlist('platforms'),
        'developer_name': request.values.getlist('developer_name'),
        'publisher_name': request.values.getlist('publisher_name'),
        'release_date': request.form.get('release_date'),
        'affiliate_link': request.form.get('affiliate_link'),
        'game_summ': request.form.get('game_summ')
    })

    return redirect(url_for('get_admin_panel'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('edit_category.html',
                           category=mongo.db.categories.find_one(
                               {'_id': ObjectId(category_id)}))


@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_admin_panel'))


@app.route('/edit_publisher/<publisher_id>')
def edit_publisher(publisher_id):
    return render_template('edit_publisher.html',
                           publisher=mongo.db.publishers.find_one(
                               {'_id': ObjectId(publisher_id)}))


@app.route('/update_publisher/<publisher_id>', methods=['POST'])
def update_publisher(publisher_id):
    publishers = mongo.db.publishers
    publishers.update({'_id': ObjectId(publisher_id)},
                      {
        'publisher_name': request.form.get('publisher_name'),
        'publisher_desc': request.form.get('publisher_desc'),
        'publisher_founding_date': request.form.get('publisher_founding_date')

    })
    return redirect(url_for('get_admin_panel'))


@app.route('/edit_developer/<developer_id>')
def edit_developer(developer_id):
    return render_template('edit_developer.html',
                           developer=mongo.db.developers.find_one(
                               {'_id': ObjectId(developer_id)}))


@app.route('/update_developer/<developer_id>', methods=['POST'])
def update_developer(developer_id):
    developers = mongo.db.developers
    developers.update({'_id': ObjectId(developer_id)},
                      {
        'developer_name': request.form.get('developer_name'),
        'developer_desc': request.form.get('developer_desc'),
        'developer_founding_date': request.form.get('developer_founding_date')

    })
    return redirect(url_for('get_admin_panel'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

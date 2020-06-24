import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import bcrypt


# checks if the env.py file exists, if true it imports the file,
# used to get the enviramental variables
if path.exists('env.py'):
    import env

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "Game_Score"
COLLECTION_NAME = "games"


app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'Game_score'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')


mongo = PyMongo(app)


# User authentication


@app.route('/')
def index():
    # if 'username' in session:
    #     flash('You are logged in as ' + session['username'])

    return redirect(url_for('view_games'))


@app.route('/home')
def home_page():
    return render_template('home_page.html',
                           games=mongo.db.games.find())


@app.route('/users/registration', methods=["POST", "GET"])
def register_user():
    return render_template('user_registration.html',
                           users=mongo.db.users.find())


@app.route('/users/insert', methods=["POST", "GET"])
def register():

    if request.method == 'POST':
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
            return redirect(url_for('index'))
        flash('That Username already exists!')
        return redirect(url_for('register_user'))
    return redirect(url_for('user_login'))


@app.route('/users/login', methods=["POST", "GET"])
def user_login():
    return render_template('user_login.html',
                           users=mongo.db.users.find())


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
    return 'Invalid username/password combination'


@app.route('/users/logout')
def logout():
    session.pop("username")
    flash('You were successfully logged Out')

    return redirect(url_for('get_admin_panel'))

# Initial load page


@ app.route('/get_admin_panel')
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

# Routing and functions to add to the database


@ app.route('/add_game')
def add_game():
    if 'username' in session:
        return render_template('addgame.html',
                               categories=mongo.db.categories.find(),
                               developers=mongo.db.developers.find(),
                               publishers=mongo.db.publishers.find(),
                               platforms=mongo.db.platforms.find())
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_game', methods=['GET', 'POST'])
def insert_game():
    games = mongo.db.games
    platforms = request.values.getlist('platforms')
    game_categories = request.values.getlist('game_categories')
    game_name = request.form['game_name']
    game_summ = request.form['game_summ']
    developer_name = request.form.get('developer_name')
    publisher_name = request.form.get('publisher_name')
    release_date = request.form['release_date']
    affiliate_link = request.form['affiliate_link']
    game_added_by = session['username']

    games.insert_one({
        'game_name': game_name,
        'game_categories': game_categories,
        'platforms': platforms,
        'game_summ': game_summ,
        'developer_name': developer_name,
        'publisher_name': publisher_name,
        'release_date': release_date,
        'affiliate_link': affiliate_link,
        'game_added_by': game_added_by
    })

    return redirect(url_for('view_games'))


@ app.route('/add_category')
def add_category():
    if 'username' in session:
        return render_template('addcategory.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name'),
                    'added_by': session['username']}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_admin_panel'))


@ app.route('/add_publisher')
def add_publisher():
    if 'username' in session:
        return render_template('add_publisher.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_publisher', methods=['GET', 'POST'])
def insert_publisher():
    publishers = mongo.db.publishers
    publisher_name = request.form.get('publisher_name')
    publisher_desc = request.form.get('publisher_desc')
    publisher_founding_date = request.form.get('publisher_founding_date')
    added_by = session['username']
    publishers.insert_one({
        'publisher_name': publisher_name,
        'publisher_desc': publisher_desc,
        'publisher_founding_date': publisher_founding_date,
        'added_by': added_by

    })
    return redirect(url_for('get_admin_panel'))


@ app.route('/add_review')
def add_review():
    if 'username' in session:
        return render_template('add_review.html',
                               games=mongo.db.games.find())
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_review', methods=['POST', 'GET'])
def insert_review():
    reviews = mongo.db.reviews
    review_game = request.form.get('review_game')
    review_header = request.form['review_header']
    review_author = request.form['review_author']
    review_body = request.form['review_body']
    review_date = request.form['review_date']
    review_score = request.form['review_score']
    review_by = session['username']

    reviews.insert_one({
        'review_game': review_game,
        'review_header': review_header,
        'review_author': review_author,
        'review_body': review_body,
        'review_date': review_date,
        'review_score': review_score,
        'review_by': review_by
    })

    return redirect(url_for('get_admin_panel'))


@ app.route('/add_developer')
def add_developer():
    if 'username' in session:
        return render_template('add_developer.html')
    else:
        flash("Please login to access this feature!")
        return redirect(url_for('user_login'))


@ app.route('/insert_developer', methods=['GET', 'POST'])
def insert_developer():
    developers = mongo.db.developers
    developer_name = request.form.get('developer_name')
    developer_desc = request.form.get('developer_desc')
    developer_founding_date = request.form.get('developer_founding_date')
    added_by = session['username']
    developers.insert_one({
        'developer_name': developer_name,
        'developer_desc': developer_desc,
        'developer_founding_date': developer_founding_date,
        'added_by': added_by
    })
    return redirect(url_for('get_admin_panel'))


# Edit database section


@ app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    creator = the_game['game_added_by']
    if session['username'] == creator:
        return render_template('editgame.html', game=the_game,
                               games=mongo.db.games.find(),
                               categories=mongo.db.categories.find(),
                               developers=mongo.db.developers.find(),
                               publishers=mongo.db.publishers.find(),
                               platforms=mongo.db.platforms.find(),)

    else:
        flash('Please log in as:' + creator)
        return redirect(url_for('user_login'))


@ app.route('/update_game/<game_id>', methods=["POST", "GET"])
def update_game(game_id):
    games = mongo.db.games
    games.update({'_id': ObjectId(game_id)},
                 {
        'game_name': request.form.get('game_name'),
        'game_categories': request.form.getlist('game_categories'),
        'platforms': request.values.getlist('platforms'),
        'developer_name': request.form.get('developer_name'),
        'publisher_name': request.form.get('publisher_name'),
        'release_date': request.form.get('release_date'),
        'affiliate_link': request.form.get('affiliate_link'),
        'game_summ': request.form.get('game_summ')
    })
    return redirect(url_for('get_admin_panel'))


@ app.route('/edit_category/<category_id>')
def edit_category(category_id):
    the_category = mongo.db.categories.find_one(
        {'_id': ObjectId(category_id)})
    creator = the_category['added_by']
    if session['username'] == creator:
        return render_template('edit_category.html',
                               category=the_category)
    else:
        flash('Please log in as   ' + creator)
        return redirect(url_for('user_login'))


@ app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_admin_panel'))


@ app.route('/edit_publisher/<publisher_id>')
def edit_publisher(publisher_id):
    the_publisher = mongo.db.publishers.find_one(
        {'_id': ObjectId(publisher_id)})
    creator = the_publisher['added_by']
    if session['username'] == creator:
        return render_template('edit_publisher.html',
                               publisher=the_publisher)
    else:
        flash('Please login as  ' + creator)
        return redirect(url_for('user_login'))


@ app.route('/update_publisher/<publisher_id>', methods=['POST'])
def update_publisher(publisher_id):
    publishers = mongo.db.publishers
    publishers.update({'_id': ObjectId(publisher_id)},
                      {
        'publisher_name': request.form.get('publisher_name'),
        'publisher_desc': request.form.get('publisher_desc'),
        'publisher_founding_date': request.form.get('publisher_founding_date')

    })
    return redirect(url_for('get_admin_panel'))


@ app.route('/edit_developer/<developer_id>')
def edit_developer(developer_id):
    the_developer = mongo.db.developers.find_one(
        {'_id': ObjectId(developer_id)})
    creator = the_developer['added_by']
    if session['username'] == creator:
        return render_template('edit_developer.html',
                               developer=the_developer)
    else:
        flash('Please login as :  ' + creator)
        return redirect(url_for('user_login'))


@ app.route('/update_developer/<developer_id>', methods=['POST'])
def update_developer(developer_id):
    developers = mongo.db.developers
    developers.update({'_id': ObjectId(developer_id)},
                      {
        'developer_name': request.form.get('developer_name'),
        'developer_desc': request.form.get('developer_desc'),
        'developer_founding_date': request.form.get('developer_founding_date')

    })
    return redirect(url_for('get_admin_panel'))


@ app.route('/edit_review/<review_id>')
def edit_review(review_id):
    the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    creator = the_review['review_by']
    all_games = mongo.db.games.find()
    print(creator)
    if session['username'] == creator:
        return render_template('edit_review.html',
                               review=the_review,
                               games=all_games)
    else:
        flash('please login as:' + creator)
        return redirect(url_for('user_login'))


@ app.route('/update_review/<review_id>', methods=['POST'])
def update_review(review_id):
    reviews = mongo.db.reviews
    reviews.update({'_id': ObjectId(review_id)},
                   {
        'review_game': request.form.get('review_game'),
        'review_header': request.form.get('review_header'),
        'review_author': request.form.get('review_author'),
        'review_body': request.form.get('review_body'),
        'review_date': request.form.get('review_date'),
        'review_score': request.form.get('review_score')
    })
    return redirect(url_for('get_admin_panel'))


# View section

@ app.route('/games')
def view_games():
    return render_template('view_games.html',
                           games=mongo.db.games.find(),
                           categories=mongo.db.categories.find())


@ app.route('/developers')
def view_developers():
    return render_template('view_developers.html',
                           developers=mongo.db.developers.find())


@ app.route('/publishers')
def view_publishers():
    return render_template('view_publishers.html',
                           publishers=mongo.db.publishers.find())


@ app.route('/game/review/<game_id>')
def view_game_review(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    all_reviews = mongo.db.reviews.find()
    return render_template('view_game_review.html',
                           reviews=all_reviews,
                           game=the_game)


@ app.route('/games/developer/<developer_name>')
def view_games_by_developer(developer_name):
    return render_template('view_games.html',
                           games=mongo.db.games.find({"developer_name":
                                                      developer_name}))


@ app.route('/games/publisher/<publisher_name>')
def view_games_by_publisher(publisher_name):
    return render_template('view_games.html',
                           games=mongo.db.games.find({"publisher_name":
                                                      publisher_name}))


@ app.route('/games/category/<category_name>')
def view_games_by_category(category_name):
    return render_template('view_games.html',
                           games=mongo.db.games.find({"game_categories":
                                                      category_name}),
                           categories=mongo.db.categories.find())


if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

import os
from os import path
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

# checks if the env.py file exists, if true it imports the file,
# used to get the enviramental variables
if path.exists('env.py'):
    import env


app = Flask(__name__)
MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME = "Game_Score"
COLLECTION_NAME = "games"
app.config["MONGO_DBNAME"] = DBS_NAME
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
mongo = PyMongo(app)

# Route Imports

# home_page, get_admin_panel
from general import *

# register_user, register, user_login, login, logout
from authentication import *

# add_game, insert_game, view_games, view_games_by_category,
# edit_game, update_game
from games import *

# add_category, insert_category, edit_category, update_category
from categories import *

# add_publisher, insert_publisher, view_publishers, view_publisher_games
# edit_publisher, update_publisher
from publisher import *

# add_developer, insert_developer, edit_developer, update_developer,
# view_developers, view_developer_games
from developer import *

# add_review, insert_review, review_by_game, view_game_review,
# edit_review, update_review
from reviews import *

if __name__ == '__main__':
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get('DEBUG_MODE'))
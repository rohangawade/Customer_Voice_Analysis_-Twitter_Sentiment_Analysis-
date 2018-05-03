from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Put your secret key here'
DB_NAME = 'ADM'
ip='127.0.0.1'
port=27017
DATABASE = MongoClient(ip,port)[DB_NAME]
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True

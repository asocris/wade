from this import d
from flask import Flask, request, jsonify, make_response
from db.db import DBConnection
import uuid
import jwt
import datetime
from functools import wraps
from flask_cors import CORS
import rdf
from pprint import pprint
from rdflib.plugins.sparql.results.txtresults  import TXTResultSerializer
import json
import io

app = Flask(__name__)
CORS(app)
app.config.update(
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf',
    FLASK_ENV='development'
)
db = DBConnection()


#
users = db.get_all_users()
for user in users:
    rdf.addUser(user) 
#

def print_result_set(rs):
    res = ''
    #stream = io.StringIO("")
    for r in rs:
        res = res + str(r) + "\n"#TXTResultSerializer(rs).serialize(stream, 'utf-8') + "\n"
    return res

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.get_user_by_username(data['username'])
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/', methods=['POST'])
def hello_world():
    content = request.json
    query = content['query']
    res = ''
    for r in rdf.freeSparql(query):
        res = res + str(r) + "\n"
    return res
    users = db.get_all_users()
    response = {}
    response['usernames'] = users
    return response


@app.route('/login', methods=['POST'])
def login():
    content = request.json
    
    user = db.get_user_by_username(content['username'])
    if user is not None:
        if(user['password'] != content['password']):
            return make_response('Could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})
        else:
            token = jwt.encode({'username': user['username']} , app.config['SECRET_KEY'])  
            return jsonify({'token' : token.decode('UTF-8'), 'username': user['username'], 'fullname': user['fullname']}) 
    else:
        return make_response('Could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@app.route('/friends/add', methods=['POST'])
@token_required
def add_friend(current_user):
    content = request.json
    user_username = current_user['username']
    friend_username = content['friendUsername']
    rdf.addFriend(user_username, friend_username)
    return ('', 201)

@app.route('/movies/watched/add', methods=['POST'])
@token_required
def add_movie(current_user):
    content = request.json
    user_username = current_user['username']
    movie_name = content['movieName']
    rdf.addMovie(user_username, movie_name)
    return ('', 201)


@app.route('/movies', methods=['GET'])
def search_movie():
    args = request.args
    movieName = args.get("name")
    result = rdf.getMovie(movieName)
    return print_result_set(result)

@app.route('/friends/watched', methods=['GET'])
@token_required
def get_watched_by_friends(current_user):
    user_username = current_user['username']
    
    result = rdf.getWatchedByFriends(user_username)
    return print_result_set(result)






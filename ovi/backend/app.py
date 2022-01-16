from this import d
from flask import Flask, request, jsonify, make_response
from db.db import DBConnection
import uuid
import jwt
import datetime
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.update(
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf',
    FLASK_ENV='development'
)
db = DBConnection()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = db.get_user_by_username(data['username'])
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/')
@token_required
def hello_world(current_user):
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

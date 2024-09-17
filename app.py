"""
Copyright 2024 Haavard Nakling

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


from tinydb import TinyDB, Query
from flask import Flask, jsonify, render_template, request
from bcrypt import hashpw, checkpw, gensalt
from uuid import uuid4
from time import sleep
from random import randrange

app = Flask(__name__, template_folder='templates', static_folder='static')
db = TinyDB('db.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-queue', methods=['GET'])
def get_queue():
    queue = db.all()
    return jsonify(queue)

@app.route('/add-to-queue', methods=['POST'])
def add_to_queue():
    data = request.json
    name = data.get('name')
    if name:
        db.insert({'name':name})
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'error': 'Name is required'}), 400

@app.route('/clear-queue', methods=['POST'])
def clear_queue():
    db.truncate()
    return jsonify({'success': True}), 200

@app.route('/remove-from-queue', methods=['POST'])
def remove_from_queue():
    data = request.json
    name = data.get('name')

    if name:
        User = Query()
        db.remove(User.name == name)
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Name is required'}), 400

@app.route('/add-new-user', methods=['POST'])
def add_new_user():
    data = request.json
    username = data.get('username')
    pw = data.get('password')
    User = Query()
    user_id = uuid4()
    while db.search(User.user_id.exists()): user_id = uuid4() # Very low probability of happening

    if db.search(User.username == username):
        return jsonify({'success': False, 'error': 'Name is already taken'}), 400
    else:
        hashed_pw = hashpw(pw.encode('utf-8'), gensalt(rounds=12))
        db.insert({'username':username, 'hashed_pw':hashed_pw.decode('utf-8'), 'user_id':user_id})
        return jsonify({'success': True}), 200

@app.route('/log-in', methods=['GET'])
def log_in():
    data = request.json
    username = data.get('username')
    pw = data.get('password')
    User = Query()
    if not db.search(User.username == username): 
        sleep(0.245+randrange(0,0.01,100)) # To mimic bcrypt time
        return jsonify({'success': False, 'error': 'Username or password is wrong'}), 400

    if not checkpw(password=pw.encode('utf-8'), hashed_password=(db.get(User.username==username)['hashed_pw']).encode('utf-8')): return jsonify({'success': False, 'error': 'Username or password is wrong'}), 400
    else:
        return jsonify({'success': True, 'user_id': (User.username == username)['user_id']}), 200
        

if __name__ == '__main__':
    app.run()

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

app = Flask(__name__, template_folder='templates')
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
    name = data.get('name')  # Get the 'name' from the request body

    if name:
        # Create a query object to search for the entry with the given name
        User = Query()
        db.remove(User.name == name)  # Remove the user with the matching name
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'error': 'Name is required'}), 400
    
if __name__ == '__main__':
    app.run(debug=True)

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

if __name__ == '__main__':
    app.run(debug=True)
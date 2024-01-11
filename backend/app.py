# app.py

from flask import Flask, jsonify, request, abort
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# SQLite3 Database Configuration
DATABASE = 'garage.db'

def create_table():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                color TEXT NOT NULL,
                model TEXT NOT NULL,
                image TEXT
            )
        ''')
        connection.commit()

# Initialize database table
create_table()

# Helper function to execute SQL queries
def query_db(query, args=(), one=False):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute(query, args)
        result = cursor.fetchone() if one else cursor.fetchall()
        return result

# API Endpoints

@app.route('/api/cars', methods=['GET'])
def get_all_cars():
    cars = query_db('SELECT * FROM cars')
    return jsonify({'cars': cars})

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = query_db('SELECT * FROM cars WHERE id = ?', (car_id,), one=True)
    if car:
        return jsonify({'car': car})
    else:
        abort(404, 'Car not found')

@app.route('/api/cars', methods=['POST'])
def add_car():
    if not request.json or 'color' not in request.json or 'model' not in request.json:
        abort(400, 'Color and model are required fields for adding a car.')

    color = request.json['color']
    model = request.json['model']
    image = request.json.get('image', None)

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO cars (color, model, image) VALUES (?, ?, ?)', (color, model, image))
        connection.commit()

    return jsonify({'message': 'Car added successfully'}), 201

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = query_db('SELECT * FROM cars WHERE id = ?', (car_id,), one=True)
    if not car:
        abort(404, 'Car not found')

    update_data = request.json
    print(car[0])
    color = update_data.get('color', car[1])
    model = update_data.get('model', car[2])
    image =  update_data.get('image', car[3])

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE cars SET color = ?, model = ?, image = ? WHERE id = ?
        ''', (color, model, image, car_id))
        connection.commit()

    return jsonify({'message': 'Car updated successfully'})

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = query_db('SELECT * FROM cars WHERE id = ?', (car_id,), one=True)
    if not car:
        abort(404, 'Car not found')

    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        connection.commit()

    return jsonify({'message': 'Car deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

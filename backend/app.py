# app.py

from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Car Model
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))

# Create the database tables


# API Endpoints

@app.route('/api/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    print(cars)
    return jsonify({'cars': [{'id': car.id, 'color': car.color, 'model': car.model, 'image': car.image} for car in cars]})

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = Car.query.get(car_id)
    if car:
        return jsonify({'car': {'id': car.id, 'color': car.color, 'model': car.model, 'image': car.image}})
    else:
        abort(404, 'Car not found')

@app.route('/api/cars', methods=['POST'])
def add_car():
    if not request.json or 'color' not in request.json or 'model' not in request.json:
        abort(400, 'Color and model are required fields for adding a car.')

    color = request.json['color']
    model = request.json['model']
    image = request.json.get('image', None)
    print(color)
    new_car = Car(color=color, model=model, image=image)
    db.session.add(new_car)
    db.session.commit()

    return jsonify({'message': 'Car added successfully'}), 201


@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        abort(404, 'Car not found')

    update_data = request.json
    car.color = update_data.get('color', car.color)
    car.model = update_data.get('model', car.model)
    car.image = update_data.get('image', car.image)

    db.session.commit()

    return jsonify({'message': 'Car updated successfully'})

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get(car_id)
    if not car:
        abort(404, 'Car not found')

    db.session.delete(car)
    db.session.commit()

    return jsonify({'message': 'Car deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

# app.py

from flask import Flask, jsonify, request, abort, send_from_directory,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configure Flask-SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///garage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Car Model
# app.py

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='cars')




# Create the database tables


# API Endpoints

from flask import url_for

# ... (existing code) ...
app.config['UPLOAD_FOLDER'] = 'uploads'
@app.route('/api/cars', methods=['GET'])
def get_all_cars():
    cars = Car.query.all()
    car_list = []

    for car in cars:
        car_data = {
            'id': car.id,
            'color': car.color,
            'model': car.model,
            'image': url_for('get_car_image', filename=car.image) if car.image else None
        }
        car_list.append(car_data)

    return jsonify({'cars': car_list})

@app.route('/uploads/<filename>')
def get_car_image(filename):
    # Adjust the path based on your project structure
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
    car = Car.query.get(car_id)
    if car:
        return jsonify({'car': {'id': car.id, 'color': car.color, 'model': car.model, 'image': car.image}})
    else:
        abort(404, 'Car not found')

@app.route('/api/cars', methods=['POST'])
def add_car():
    if not request.form or 'color' not in request.form or 'model' not in request.form:
        abort(400, 'Color and model are required fields for adding a car.')

    color = request.form['color']
    model = request.form['model']
    user = request.form['user_id']
    image = request.files.get('image', None)

    # Validate file type, size, etc., if needed

    # Save the image to the server, you may need to adjust the path
    if image:
        image.save(f'uploads/{image.filename}')

    new_car = Car(color=color, model=model, image=image.filename if image else None,user_id=user)
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


@app.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email
        }
        user_list.append(user_data)

    return jsonify({'users': user_list})

# ... (existing code) ...

# Function to add a new car
@app.route('/api/cars11', methods=['POST'])
def addCar():
    # Get user details
    print("-----------------------------------------------------------------------------")
    user_id = request.json['user_id']
    # user_id = request.form.get('user_Id')
    # On the server side
    user_id = request.form.get('user_id')

    # print(request.json)
    print(user_id)
    print("-----------------------------------------------------------------------------")
    return jsonify({'message': 'Car added successfully'}), 201
    user = User.query.get(user_id)
    
    # Check if the user exists
    if not user:
        abort(404, 'User not found')
    
    # Add the car to the database
    color = request.json['color']
    model = request.json['model']
    image = request.files.get('image', None)

    # Validate file type, size, etc., if needed

    # Save the image to the server
    if image:
        image.save(f'uploads/{image.filename}')

    new_car = Car(color=color, model=model, image=image.filename if image else None, user=user)
    db.session.add(new_car)
    db.session.commit()

    return jsonify({'message': 'Car added successfully'}), 201

@app.route('/api/users', methods=['POST'])
def addUser():
    name = request.json['name']
    email = request.json['email']

    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully'}), 201

# ... (existing code) ...


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

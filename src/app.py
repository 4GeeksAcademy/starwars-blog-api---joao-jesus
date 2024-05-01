"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, People, Planets, Vehicles, Favorites, User
from flask import g
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_all_user():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    all_people = list(map(lambda x: x.serialize(), people))
    
    return jsonify(all_people), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({"error": "Person not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_all_planets():

    planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), planet))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet():

    planet = Planets.query.get(id)
   
    return jsonify(planet), 200

@app.route('/vehicles', methods=['GET'])
def get_all_vehicles():
    vehicle = Vehicles.query.all()
    all_vehicles = list(map(lambda x: x.serialize(), vehicle))
    
    return jsonify(all_vehicles), 200

@app.route('/vehicles/<int:vehicles_id>', methods=['GET'])
def get_vehicle():
    vehicle = Vehicles.query.get(id)
    
    
    return jsonify(vehicle), 200

@app.route('/users', methods=['GET'])
def get_favorites():
    user = Users.query.all()
    Users = list(map(lambda x: x.serialize(), user))
    
    return jsonify(Users), 200

@app.route('/users/favorites', methods=['GET'])
def get_favorite():
    favorites = Favorites.query.all()
    Favorite = list(map(lambda x: x.serialize(), favorites))
    
    return jsonify(Favorite), 200




@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    # Get the current user from Flask global context
    current_user = g.user
    
    
    if current_user is None:
        return jsonify({"error": "User not authenticated"}), 401

    # Get the user ID
    user_id = current_user.id

    # Check if the planet exists
    planet = Planets.query.get(planet_id)
    if planet is None:
        return jsonify({"error": "Planet not found"}), 404

    # Check if the favorite already exists for this user and planet
    existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Planet already favorited"}), 400

    # Create a new favorite entry
    favorite = Favorites(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet added successfully"}), 200

@app.route('/favorites/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # Get the current user from Flask global context
    current_user = g.user
    
    
    if current_user is None:
        return jsonify({"error": "User not authenticated"}), 401

    # Get the user ID
    user_id = current_user.id

    # Check if the planet exists
    people = People.query.get(people_id)
    if people is None:
        return jsonify({"error": "People not found"}), 404

    # Check if the favorite already exists for this user and planet
    existing_favorite = Favorites.query.filter_by(user_id=user.id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"error": "People already favorited"}), 400

    # Create a new favorite entry
    favorite = Favorites(user_id=user.id, people_id=people.id)
    db.session.add(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite character added successfully"}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

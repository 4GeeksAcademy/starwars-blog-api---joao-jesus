from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False)
    people = db.relationship('People', lazy=True)
    planets = db.relationship('Planets', lazy=True)
    vehicles = db.relationship('Vehicles', lazy=True)
    favorites = db.relationship('Favorites', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    age = db.Column(db.Integer)
    height = db.Column(db.Integer)
    gender = db.Column(db.String(250))
    eyecolor = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    owner = db.relationship('User', backref=db.backref('owned_people', lazy=True))
   

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "height": self.height,
            "gender": self.gender,
            "eyecolor": self.eyecolor,
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    diameter = db.Column(db.Float)
    gravity = db.Column(db.Float)
    population = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    people = db.relationship('People', backref='planet', lazy=True)

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "population": self.population,
        }

class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    speed = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
   

    def __repr__(self):
        return '<Vehicles %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "passengers": self.passengers,
            "speed": self.speed,
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    favorite_vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    favorite_people_id = db.Column(db.Integer, db.ForeignKey('people.id'))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "favorite_planet_id": self.favorite_planet_id,
            "favorite_vehicle_id": self.favorite_vehicle_id,
            "favorite_people_id": self.favorite_people_id,
        }

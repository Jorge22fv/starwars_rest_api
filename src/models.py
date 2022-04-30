from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
# pipenv run migrate
# pipenv run upgrade
# -> efectuar cambios en la base de datos
# mysql;  use example; show tables; exit;


class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(20), unique=False, nullable=True)
    height = db.Column(db.Integer, unique=False, nullable=True)
    mass = db.Column(db.Float, unique=False, nullable=True)

    def serialize(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "gender": self.gender,
            "height": self.height,
            "mass": self.mass
            # do not serialize the password, its a security breach
        }


class Fav_people(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid_people = db.Column(db.Integer, db.ForeignKey('people.uid'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    people = db.relationship('People')
    user = db.relationship('User')

    def serialize(self):
        return {
            "uid_people": self.uid_people,
            "id_user": self.id_user,
            "id": self.id,
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=True)
    climate = db.Column(db.String(20), unique=False, nullable=True)
    gravity = db.Column(db.Float, unique=False, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "gravity": self.gravity
        }

class Fav_planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_planets = db.Column(db.Integer, db.ForeignKey('planets.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    planets = db.relationship('Planets')
    user =  db.relationship('User')
    
    def serialize(self):
        return{
            "id": self.id,
            "id_planets": self.id_planets,
            "id_user": self.id_user
        }


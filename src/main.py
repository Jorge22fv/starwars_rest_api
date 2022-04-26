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
from models import db, User, People, Planets, Fav_people, Fav_planets
#from models import Person

# elementos de configuración
app = Flask(__name__)  # instanciar una aplicación Flask
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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
def getUser():
    all_user = User.query.all()
    user_arr = list(map(lambda x: x.serialize(), all_user))

    return jsonify({"Resultados": user_arr})


@app.route('/people', methods=['GET'])
def getPeople():
    all_people = People.query.all()
    arreglo_people = list(map(lambda x: x.serialize(), all_people))

    return jsonify({"Resultados": arreglo_people})


@app.route('/people/<int:people_id>', methods=['GET'])
def getPeopleID(people_id):
    one_people = People.query.get(people_id)
    if one_people:
        return jsonify({"personaje": one_people.serialize()})
    else:
        return "error, no encontrado"


@app.route('/fav_people', methods=['GET'])
def getFav_people():
    all_favpeople = Fav_people.query.all()
    favpeople_arr = list(map(lambda x: x.serialize(), all_favpeople))

    return jsonify({"Resultados": favpeople_arr})


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def addFavPeople(people_id):

    user = request.get_json()  # {id:1}
    # chequear si existe el usuario
    # instanciar un nuevo favorito
    if checkUser:
        newFav = Fav_people()
        newFav.id_user = user['id']
        newFav.uid_people = people_id

        db.session.add(newFav)
        db.session.commit()
        return("todo salió bien :D")
    else:
        return("user no existe")


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def deleteFavPeople(people_id):
    user = request.get_json()  # {id:1}
    allFavs = Fav_people.query.filter_by(
        id_user=user['id'], uid_people=people_id).all()

    for i in allFavs:
        db.session.delete(i)
    db.session.commit()

    return('todo salio ok')


@app.route('/planets', methods=['GET'])
def getPlanets():
    all_planets = Planets.query.all()
    planets_arr = list(map(lambda x: x.serialize(), all_planets))

    return jsonify({"Resultados": planets_arr})


@app.route('/planets/<int:planets_id>', methods=['GET'])
def getPlanetsID(planets_id):
    one_planet = Planets.query.get(planets_id)
    if one_planet:
        return jsonify({"planet": one_planet.serialize()})
    else:
        return "error, no encontrado"


@app.route('/fav_planets', methods=['GET'])
def getFav_planets():
    all_favplanets = Fav_planets.query.all()
    favplanets_arr = list(map(lambda x: x.serialize(), all_favplanets))

    return jsonify({"Resultados": favplanets_arr})

"""
@app.route('/favorite/planets/<int:planets_id>', methods=['POST'])
def addFavPlanet(planets_id):

    user = request.get_json()  
    if checkUser:
        newFavPlanet = Fav_planets()
        newFavPlanet.id_user = user['id']
        newFavPlanet.id_planets = planets_id

        db.session.add(newFavPlanet)
        db.session.commit()
        return("todo salió bien :D")
    else:
        return("user no existe")


@app.route('/favorite/planets/<int:planets_id>', methods=['DELETE'])
def deleteFavPlanet(planets_id):
    user = request.get_json()  # {id:1}
    allFavsPlanets = Fav_planets.query.filter_by(
        id_user=user['id'], id_planets=planets_id).all()

    for i in allFavsPlanets:
        db.session.delete(i)
    db.session.commit()

    return('todo salio ok')


"""




# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

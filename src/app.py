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
from models import db, User, Character,Planet,Favorites
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
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


# get characters
@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    return jsonify({
        "characters": list(map(lambda item: item.serialize_character(), characters))
    }),200

#get character  
@app.route('/character/<int:theid>', methods=['GET'])
def get_character(theid):
    character = Character.query.get(theid)
    if character is None:
        return jsonify("No existe este personaje"),404
    else:
        return jsonify(character.serialize_character()),200

#get planets
@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets=Planet.query.all()
    return jsonify({
        "planets":list(map(lambda item: item.serialize_planet(),planets))
    })

#get one planet
@app.route('/planet/<int:theid>', methods=['GET'])
def get_planet(theid):
    planet=Planet.query.get(theid)
    if planet is None:
        return jsonify("No existe este personaje"),404
    else:
        return jsonify(planet.serialize_planet()),200
    
#get users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return({
        "users":list(map(lambda item: item.serialize_user(), users))
    })

# @app.route('/favorites', methods=['POST'])
# def add_favorite():
#     body=request.json
#     favorites = favorites()
#     try:
#         user_id = body['user_id']
#         planet_id = body['planet_id']
#         character_id = body['character_id']
        
#         if user_id is None:
#             return jsonify('Usuario no existe'),404
#         if planet_id is None and character_id is None:
#             return jsonify('No existe el favorito que deseas agregar'),404
        
#         favorites.user_id=user_id
#         favorites.planet_id=planet_id
#         favorites.character_id=character_id

#         db.session.add(favorites)
#         db.session.commit()
#         return jsonify('Guardado')


#     except Exception as error:
#         return jsonify("Error en el servidor"),500




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

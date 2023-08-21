"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    response_body = jackson_family.get_all_members()
    
    if response_body:
        return jsonify(response_body), 200
    else:
        return "Ocurrió algún error", 404

@app.route('/member/<int:member_id>', methods=['GET'])
def member_id_get(member_id):

    member = jackson_family.get_member(member_id)

    if member:
        return jsonify(member), 200
    else:
        return "Ocurrió algún error", 404

@app.route('/member', methods=['POST'])
def member_post():
    
    data = request.json 
    member = {
        "first_name": data.get("first_name"),
        "age": data.get("age"),
        "lucky_number": data.get("lucky_number")
    }
    jackson_family.add_member(member)
    
    if jackson_family:
        return "Miembro agregado", 200
    else:
        return "No se agregó el miembro ocurrió algún error", 404

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member_id(member_id):

    result = jackson_family.delete_member(member_id)

    if result:
        return "Eliminado con éxito", 200
    else:
        return "No se encontró el miembro ocurrió algún error", 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
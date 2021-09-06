from functools import wraps
from flask import Blueprint, json, jsonify, request
from flask_migrate import current
from dc_character_inventory.helpers import token_required
from dc_character_inventory.models import db, User, Character, character_schema, characters_schema

api = Blueprint('api',__name__,url_prefix='/api')

@api.route('/getdata')
@token_required
def get_data(current_user_token):
    return { 'some' : 'value'}

# Create character endpoint
@api.route('/characters', methods =['POST'])
@token_required
def create_character(current_user_token):
    name = request.json['name']
    secret_identity = request.json['secret_identity']
    description = request.json['description']
    comics_appeared_in = request.json['comics_appeared_in']
    superpower = request.json['superpower']
    alignment = request.json['alignment']
    occupation = ['occupation']
    date_created = ['date_created']
    user_token = current_user_token.token

    character = Character(name, secret_identity, description, comics_appeared_in, superpower, alignment, occupation, date_created, user_token)
    db.session.add(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)

# Retrieve all characters endpoint
@api.route('/characters', methods=['GET'])
@token_required
def get_characters(current_user_token):
    owner = current_user_token.token
    characters = Character.Query.filer_by(user_token=owner).all()
    response = characters_schema.dump(characters)
    return jsonify(response)

# Retrieve one character endpoint
@api.route('/characters/<id>', methods = ['GET'])
@token_required
def get_character(current_user_token, id):
    owner = current_user_token
    character = Character.query.get(id)
    response = character_schema.dump(character)
    return jsonify(response)

# Update chracter endpoint
@api.route('/characters/<id>', methods = ['POST', 'PUT'])
@token_required
def update_chracter(current_user_token, id):
    character = Character.query.get(id)

    character.name = request.json['name']
    character.secret_identity = request.json['secret_identity']
    character.description = request.json['description']
    character.comics_appeared_in = request.json['comics_appeared_in']
    character.superpower = request.json['superpower']
    character.alignment = request.json['alignment']
    character.occupation = ['occupation']
    character.date_created = ['date_created']
    character.user_token = current_user_token.token

    db.session.commit()
    response = character_schema.dump(character)
    return jsonify(response)

# Delete drone endpoint
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_character(current_user_token, id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()

    response = character_schema.dump(character)
    return jsonify(response)
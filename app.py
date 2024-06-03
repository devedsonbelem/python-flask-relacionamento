from flask import Flask, request, jsonify
from flasgger import Swagger
import sys
import os

from model.users import Users
from model.endereco import Endereco
from repository.file_repository import Repositories

app = Flask(__name__)

definitions = {
    "User": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"}
        }
    },
    "Endereco": {
        "type": "object",
        "properties": {
            "endereco_id": {"type": "string"},
            "logradouro": {"type": "string"},
            "bairro": {"type": "string"},
            "user_id": {"type": "string"}
        }
    }
}

swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "API Documentation",
        "description": "API Documentation",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http", "https"],
    "definitions": definitions
})

repository = Repositories('database.db')

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Get user by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: string
        required: true
        description: The user ID
    responses:
      200:
        description: A user object
        schema:
          id: User
          properties:
            id:
              type: string
              description: The user ID
            name:
              type: string
              description: The user's name
            email:
              type: string
              description: The user's email
      404:
        description: User not found
      500:
        description: User object does not have a user_id attribute
    """
    user = repository.get_user_by_id(user_id)
    if user:
        if hasattr(user, 'user_id'):
            return jsonify({'id': user.user_id, 'name': user.name, 'email': user.email})
        else:
            return 'User object does not have a user_id attribute', 500
    return 'User not found', 404

@app.route('/users', methods=['GET'])
def list_users():
    """
    List all users
    ---
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    users = repository.get_all_users()
    return jsonify([{'id': user.user_id, 'name': user.name, 'email': user.email} for user in users])

@app.route('/add_user', methods=['POST'])
def add_user():
    """
    Add a new user
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          id: User
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: User created
    """
    data = request.json
    user = Users(name=data['name'], email=data['email'])
    user_data = repository.add_user(user)
    return jsonify(user_data), 201

@app.route('/add_address', methods=['POST'])
def add_endereco():
    """
    Add a new address
    ---
    parameters:
      - name: address
        in: body
        required: true
        schema:
          id: Endereco
          required:
            - logradouro
            - bairro
            - user_id
          properties:
            logradouro:
              type: string
            bairro:
              type: string
            user_id:
              type: string
    responses:
      201:
        description: Address created
    """
    data = request.json
    endereco = Endereco(logradouro=data['logradouro'], bairro=data['bairro'], user_id=data['user_id'])
    endereco_data = repository.add_endereco(endereco)
    return jsonify(endereco_data), 201

@app.route('/endereco/<string:address_id>', methods=['GET'])
def get_address_one(address_id):
    """
    Get address by ID
    ---
    parameters:
      - name: address_id
        in: path
        type: string
        required: true
        description: The address ID
    responses:
      200:
        description: An address object
        schema:
          id: Endereco
          properties:
            endereco_id:
              type: string
            logradouro:
              type: string
            bairro:
              type: string
            user_id:
              type: string
      404:
        description: Address not found
      500:
        description: Address object does not have a user_id attribute
    """
    endereco = repository.get_endereco_by_id(address_id)
    if endereco:
        if hasattr(endereco, 'endereco_id'):
            return jsonify({'endereco_id': endereco.endereco_id, 'logradouro': endereco.logradouro, 'bairro': endereco.bairro, 'user_id': endereco.user_id})
        else:
            return 'Address object does not have a user_id attribute', 500
    return 'Address not found', 404

@app.route('/endereco/', methods=['GET'])
def list_address():
    """
    List all addresses
    ---
    responses:
      200:
        description: A list of addresses
        schema:
          type: array
          items:
            $ref: '#/definitions/Endereco'
    """
    enderecos = repository.get_all_enderecos()
    return jsonify([{'endereco_id': endereco.endereco_id, 'logradouro': endereco.logradouro, 'bairro': endereco.bairro, 'user_id': endereco.user_id} for endereco in enderecos])

@app.route('/innerjoin', methods=['GET'])
def get_innerjoin():
    """
    Get inner join of users and addresses
    ---
    responses:
      200:
        description: A list of users and their addresses
        schema:
          type: array
          items:
            type: object
            properties:
              endereco:
                $ref: '#/definitions/Endereco'
              user:
                $ref: '#/definitions/User'
    """
    results = repository.innerjoin()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import sys
import os
 
from  model.users import Users
from  model.endereco import Endereco
from  repository.file_repository import Repositories

app = Flask(__name__)
repository = Repositories('database.db')

 

@app.route('/users/<string:user_id>', methods=['GET'])
def get_user(user_id):
    user = repository.get_user_by_id(user_id)
    if user:
        if hasattr(user, 'user_id'):  # Check if 'user_id' attribute exists
            return jsonify({'id': user.user_id, 'name': user.name, 'email': user.email})
        else:
            return 'User object does not have a user_id attribute', 500  # Internal Server Error
    return 'User not found', 404



@app.route('/users', methods=['GET'])
def list_users():
    users =repository.get_all_users()
    return jsonify([{'id': user.user_id, 'name': user.name, 'email': user.email} for user in users])
    


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = Users(name=data['name'], email=data['email'])
    user_data =repository.add_user(user)
    return jsonify(user_data), 201



@app.route('/add_address', methods=['POST'])
def add_endereco():
    data = request.json
    endereco = Endereco(logradouro=data['logradouro'], bairro=data['bairro'], user_id=data['user_id'])
    endereco_data = repository.add_endereco(endereco)
    return jsonify(endereco_data), 201


@app.route('/endereco/<string:address_id>', methods=['GET'])
def get_address_one(address_id):
    endereco =repository.get_endereco_by_id(address_id)
    if endereco:
        if hasattr(endereco, 'endereco_id'): 
            return jsonify({'endereco_id': endereco.endereco_id, 'logradouro': endereco.logradouro, 'bairro': endereco.bairro,'user_id': endereco.user_id} )
        else:
            return 'User object does not have a user_id attribute', 500  # Internal Server Error
    return 'Endereco not found', 404

@app.route('/endereco/', methods=['GET'])
def list_address():
    enderecos =repository.get_all_enderecos()
    return jsonify([{'endereco_id': endereco.endereco_id, 'logradouro': endereco.logradouro, 'bairro': endereco.bairro,'user_id': endereco.user_id} for endereco in enderecos])


@app.route('/innerjoin', methods=['GET'])
def get_innerjoin():
    results = repository.innerjoin()
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

 
 

from flask import Flask, jsonify, request, session, make_response
import json

app = Flask(__name__)

with open('usuarios.json', 'r') as f:
    usuarios = json.load(f)

app.config['SECRET_KEY'] = 'this_key_will_be_securely_moved_to_ENVIRONMENT_VARIABLES'

properties_rows = [
  {
    'id': 1,
    "imovel_id": 1442,
    "imovel_numero": "BEH2209",
    "imovel_categoria": "GYNSUP",
    "imovel_status": "ativo",
    "imovel_contrato_inicio": "19/09/2023",
    "imovel_proprietario": "Alexandre Valladares Teixeira",
    "imovel_telefone_proprietario": "+559299988776655",
    "imovel_endereco": "Rua 1"
  },
  {
    "id": 2,
    "imovel_id": 2875,
    "imovel_numero": "BFT3015",
    "imovel_categoria": "ILCSUP",
    "imovel_status": "ativo",
    "imovel_contrato_inicio": "19/06/2024",
    "imovel_proprietario": "Alice Lene",
    "imovel_telefone_proprietario": "+5592911223344",
    "imovel_endereco": "Rua 2"
  }
]

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in usuarios and usuarios[username] == password:
        session['username'] = username
        return jsonify({'message': 'Successfully logged in!'}), 200
    else:
        return jsonify({'message': 'Invalid Credentials'}), 401

@app.route('/properties', methods=['GET'])
def get_properties():
    if 'username' in session:
        return jsonify(properties_rows)
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401

@app.route('/properties/<int:id>', methods=['GET'])
def get_property_by_id(id):
    if 'username' in session:
        for property_unit in properties_rows:
            if property_unit.get('id') == id:
                return jsonify(property_unit)
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401

@app.route('/properties', methods=['GET'])
def get_properties_by_number_and_status():
    if 'username' in session:
        imovel_numero = request.args.get('imovel_numero')
        imovel_status = request.args.get('imovel_status')

        results = []
        for property_unit in properties_rows:
            if imovel_numero and property_unit['imovel_numero'] != imovel_numero:
                continue
            if imovel_status and property_unit['imovel_status'] != imovel_status:
                continue
            results.append(property_unit)

        return jsonify(results)
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401

@app.route('/properties/<int:id>', methods=['PUT'])
def put_property_by_id(id):
    if 'username' in session:
        property_changed = request.get_json()
        for index,property_unit in enumerate(properties_rows):
            if property_unit.get('id') == id:
                properties_rows[index].update(property_changed)
                return jsonify(properties_rows[index])
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401

@app.route('/properties',methods=['POST'])
def post_property():
    if 'username' in session:
        new_property = request.get_json()
        properties_rows.append(new_property)
        return jsonify(properties_rows)
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401

@app.route('/properties/<int:id>',methods=['DELETE'])
def delete_property_by_id(id):
    if 'username' in session:
        for index, property_unit in enumerate(properties_rows):
            if property_unit.get('id') == id:
                del properties_rows[index]
        return jsonify(properties_rows)
    else:
        return jsonify({'message': 'Você não está autenticado'}), 401


app.run(port=5000, host='localhost', debug=True)
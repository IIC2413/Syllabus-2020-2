from flask import Flask, json, request
from pymongo import MongoClient


USER = "grupoXX"
PASS = "grupoXX"
DATABASE = "grupoXX"

URL = f"mongodb://{USER}:{PASS}@gray.ing.puc.cl/{DATABASE}?authSource=admin"
client = MongoClient(URL)

USER_KEYS = ['uid', 'name', 'last_name',
            'occupation', 'follows', 'age']

# Base de datos del grupo
db = client["grupoXX"]

# Seleccionamos la collección de usuarios
usuarios = db.usuarios

#Iniciamos la aplicación de flask
app = Flask(__name__)

@app.route("/")
def home():
    '''
    Página de inicio
    '''
    return "<h1>¡Hola!</h1>"

@app.route("/users")
def get_users():
    '''
    Obtiene todos los usuarios
    '''
    users = list(usuarios.find({}, {"_id": 0}))

    return json.jsonify(users)

@app.route("/users/<int:uid>")
def get_user(uid):
    '''
    Obtiene el usuario de id entregada
    '''
    user = list(usuarios.find({"uid":uid}, {"_id": 0}))

    return json.jsonify(user)


@app.route("/users", methods=['POST'])
def create_user():
    '''
    Crea un nuevo usuario en la base de datos
    Se  necesitan todos los atributos de model, a excepcion de _id
    '''

    data = {key: request.json[key] for key in USER_KEYS}

    # El valor de result nos puede ayudar a revisar
    # si el usuario fue insertado con éxito
    result = usuarios.insert_one(data)

    return json.jsonify({"success": True})


@app.route("/users", methods=['DELETE'])
def delete_user():
    '''
    Elimina el usuario de id entregada
    '''
    uid = request.json['uid']
    usuarios.remove({"uid": uid})
    return json.jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
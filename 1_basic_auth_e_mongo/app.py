from flask import Flask, request, Response
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = "sua_string_de_conexao"
mongo = PyMongo(app)

def check_auth(username, password):
    """Verifica se um nome de usuário e senha são válidos no MongoDB."""
    filtro_ = {"usuario": username, "senha": password}
    projection = {"_id": 0, "senha": 0}
    usuario = mongo.db.usuarios.find_one(filter=filtro_,
                                         projection=projection)
    
    # Se não retornou nada, usuário com essa senha não foi encontrado, ou seja, não autenticado
    if not usuario:
        return False

    return True # Usuário autenticado

@app.route('/')
def secret_page():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return Response('Você precisa se autenticar.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    # Lógica acessível apenas para usuários autenticados
    return {"msg": "Você está autenticado!"}

if __name__ == '__main__':
    app.run(debug=True)

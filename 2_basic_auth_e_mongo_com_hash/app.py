from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config["MONGO_URI"] = "sua_string_de_conexao"
mongo = PyMongo(app)

def hash_password(password):
    """Retorna o hash SHA-256 da senha."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_auth(username, password):
    """Verifica se um nome de usuário e senha são válidos no MongoDB."""
    hashed_password = hash_password(password)
    filtro_ = {"usuario": username, "senha": hashed_password}
    projection = {"_id": 0, "usuario": 0}
    usuario = mongo.db.usuarios.find_one(filter=filtro_,
                                         projection=projection)
    
    if not usuario:
        return False  # Usuário não encontrado ou senha incorreta

    return True  # Usuário autenticado


@app.route('/usuarios', methods=['POST'])
def create_user():
    # Obtém dados do corpo da requisição
    nome = request.json.get('nome')
    usuario = request.json.get('usuario')
    senha = request.json.get('senha')

    if not nome or not usuario or not senha:
        return jsonify({"error": "Nome, usuário e senha são obrigatórios"}), 400

    # Verifica se o usuário já existe
    if mongo.db.usuarios.find_one({"usuario": usuario}):
        return jsonify({"error": "Usuário já existe"}), 409

    # Aplica hash na senha antes de salvar no banco
    hashed_password = hash_password(senha)

    # Cria o documento do usuário
    user_data = {
        "nome": nome,
        "usuario": usuario,
        "senha": hashed_password
    }

    # Insere o usuário no banco de dados
    mongo.db.usuarios.insert_one(user_data)

    # Retorna sucesso
    return jsonify({"msg": "Usuário criado com sucesso!"}), 201

@app.route('/')
def secret_page():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return Response('Você precisa se autenticar.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return {"msg": "Você está autenticado!"}


if __name__ == '__main__':
    app.run(debug=True)


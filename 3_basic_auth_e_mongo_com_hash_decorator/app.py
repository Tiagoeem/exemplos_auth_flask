# app.py
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from auth import requires_auth, hash_password

app = Flask(__name__)
app.config["MONGO_URI"] = "sua_string_de_conexao"
mongo = PyMongo(app)

@app.route('/usuarios', methods=['POST'])
@requires_auth
def create_user():
    """Rota para criar um novo usuário, agora protegida por autenticação."""
    nome = request.json.get('nome')
    usuario = request.json.get('usuario')
    senha = request.json.get('senha')

    if not nome or not usuario or not senha:
        return jsonify({"error": "Nome, usuário e senha são obrigatórios"}), 400

    if mongo.db.usuarios.find_one({"usuario": usuario}):
        return jsonify({"error": "Usuário já existe"}), 409

    hashed_password = hash_password(senha)
    user_data = {"nome": nome, "usuario": usuario, "senha": hashed_password}
    mongo.db.usuarios.insert_one(user_data)
    return jsonify({"msg": "Usuário criado com sucesso!"}), 201

@app.route('/')
def public_route():
    """Rota pública que não requer autenticação."""
    return {"msg": "Página pública"}

@app.route('/secret')
@requires_auth
def secret_page():
    """Rota protegida que requer autenticação."""
    return {"msg": "Você está autenticado e pode acessar esta página protegida"}

if __name__ == '__main__':
    app.run(debug=True)



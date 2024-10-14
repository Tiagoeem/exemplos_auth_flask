# auth.py
from flask import request, Response, jsonify
from functools import wraps
import hashlib

def hash_password(password):
    """Gera um hash SHA-256 da senha."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_auth(username, password, mongo):
    """Verifica se as credenciais de usuário e senha são válidas."""
    hashed_password = hash_password(password)
    filtro_ = {"usuario": username, "senha": hashed_password}
    usuario = mongo.db.usuarios.find_one(filter=filtro_)
    return bool(usuario)

def authenticate():
    """Envia uma resposta que solicita autenticação ao usuário."""
    return Response(
        'Acesso negado. Por favor, autentique-se.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    """Decorador que protege rotas específicas com autenticação básica.
    Args:
        f (function): A função da rota Flask a ser decorada.
    Returns:
        function: A função decorada que agora inclui verificação de autenticação.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password, kwargs.get('mongo')):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

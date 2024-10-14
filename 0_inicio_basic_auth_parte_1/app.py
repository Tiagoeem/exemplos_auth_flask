from flask import Flask, request, Response
import base64

app = Flask(__name__)

def check_auth(username, password):
    """Verifica se um nome de usuário e senha fornecidos são válidos."""
    return username == "usuario_do_sistema" and password == "senha"

@app.route('/')
def secret_page():
    auth = request.authorization # Ja faz decodifica a base 64 e transforma de bytes em string
    if not auth or not check_auth(auth.username, auth.password):
        return Response('Você precisa se autenticar.', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    
    # aqui você coloca toda a lógica que só pode ser acessada por usuários autenticados
    # e o retorno é o que será exibido para o usuário, subtitua esse retorno pelo que você deseja
    return {"msg": "Você está autenticado! "} 

if __name__ == '__main__':
    app.run(debug=True)

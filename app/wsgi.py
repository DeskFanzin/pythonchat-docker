## código feito por Arthur Bubolz - 140548 e Gabriel Martins - 142356

from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send


##funções necessárias do flask e SocketIO, para que possamos criar o servidor e as rotas
##importante salientar o uso de async_mode='threading', para garantir que o servidor use multithreading, no caso
##deste trabalho as threads do gunicorn declaradas no arquivo Dockerfile nesta pasta. 

app = Flask(__name__)
app.secret_key = "mysecretkey"  # adicionando chave secreta para usar sessões
socketio = SocketIO(app, async_mode='threading', logger=True, engineio_logger=True, cors_allowed_origins="*")

## como o gunicorn, por limitação do flask-socketIO pode utilizar apenas um worker, as threads funcionarão de acordo
## com os requests feitos pelos usuários, ou seja, se um usuário enviar uma mensagem, o servidor irá criar uma thread
## para enviar a mensagem para todos os usuários conectados, e assim por diante.

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

##aqui utilizamos cookies na forma de sessões, para que possamos guardar o nome de usuário e utilizar em outras rotas

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # adicionando nome de usuário na sessão
        return redirect('/real_chat')
    else:
        return 'Caminho não encontrado!'

## INÍCIO DA UTILIZAÇÃO DE SOCKETIO
## aqui utilizamos o socketio para que possamos enviar mensagens para todos os usuários conectados ao servidor, com funções
## pré definidas pelo socketio, no caso on_connect, sendMessage e on_disconnect.

@socketio.on("connect")
def on_connect():
    username = session.get('username')
    if username:
        message = f"{username} connected!"
        send(message, broadcast=True)


##aqui é feita a formatação da mensagem que é enviada para o chat propriamente dito, com o nome de usuário e a mensagem.
## a variável message é buscada do arquivo html message.html, que é o arquivo que contém o chat em si.
## lá, utilizamos scripts em javascript para que possamos enviar a mensagem para o servidor, e servidor envia
## para todos os usuários conectados a partir do broadcast.

@socketio.on("message")
def sendMessage(message):
    username = session.get('username')  # buscando nome de usuário da sessão
    if username:
        send(f"{username}: {message}", broadcast=True)
    else:
        send(message, broadcast=True)

@socketio.on("disconnect")
def on_disconnect():
    username = session.get('username')
    if username:
        message = f"{username} disconnected!"
        send(message, broadcast=True)

@app.route("/real_chat")
def message():
    return render_template("message.html")

## Como utilizamos gunicorn, não precisamos utilizar o app.run, pois o gunicorn já faz isso por nós.
## mas, caso queira rodar o servidor sem o gunicorn, apenas rode no cmd python wsgi.py

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port='5000', debug=True, allow_unsafe_werkzeug=True)

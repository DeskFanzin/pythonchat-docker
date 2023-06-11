from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, send


app = Flask(__name__)
app.secret_key = "mysecretkey"  # adicionando chave secreta para usar sessões
socketio = SocketIO(app, async_mode='threading', logger=True, engineio_logger=True, cors_allowed_origins="*")

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username  # adicionando nome de usuário na sessão
        return redirect('/real_chat')
    else:
        return 'Caminho não encontrado!'

@socketio.on("connect")
def on_connect():
    username = session.get('username')
    if username:
        message = f"{username} connected!"
        send(message, broadcast=True)

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

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port='5000', debug=True, allow_unsafe_werkzeug=True)

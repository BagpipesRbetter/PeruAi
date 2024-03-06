#!/bin/python
import ollama
ollama.pull("llama2")

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET'])
def home(name=None):
    return render_template('index.html', name=name)

@socketio.on('message')
def handle_message(data):
    text = data['data']
    message = {'role': 'user', 'content': text}
    
    for part in ollama.chat(model='llama2', messages=[message], stream=True):
        print(part['message']['content'])
        socketio.emit('response', {'data': part['message']['content']})


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)

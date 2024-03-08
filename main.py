#!/bin/python
#change this to alter what model your using. ive had the best luck sticking with llama2 but others will work, see ollama documentation on what models are availble
_model = "llama2"
import os, webbrowser

import ollama
#downloads the correct llm model
ollama.pull(_model)
from flask import Flask, render_template
from flask_socketio import SocketIO
#initalizes the site and stream mechanisim
app = Flask(__name__, static_folder='static')
socketio = SocketIO(app, cors_allowed_origins="*")
#loads home page
@app.route('/', methods=['GET'])
def home(name=None):
    return render_template('index.html', name=name)
#handles generation
@socketio.on('message')
def handle_message(data):
    text = data['data']
    message = {'role': 'user', 'content': text}
    #generator that prints back to the sites text box
    for part in ollama.chat(model=_model , messages=[message], stream=True):
        print(part['message']['content'])
        socketio.emit('response', {'data': part['message']['content']})
#loads about page
@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')
#starts everything up
if __name__ == "__main__":
    #change the port number to anything you want that your computer isnt already using.
    url = 'http://localhost:5003'
    webbrowser.open(url)
    app.run(host="0.0.0.0", port=5003)
    


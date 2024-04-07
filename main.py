#!/bin/python
#change this to alter what model your using. ive had the best luck sticking with llama2 but others will work, see ollama documentation on what models are availble
_model = "llama2"
messages = []
import ollama
#downloads the correct llm model
if _model != "llama2":
    ollama.pull(_model)
    
from flask import Flask, render_template
from flask_socketio import SocketIO
from flaskwebgui import FlaskUI

#initalizes the site and stream mechanisim
app = Flask(__name__, static_folder='static')

socketio = SocketIO(app, cors_allowed_origins="*")
ui = FlaskUI(app, width=500, height=500) 
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

if __name__ == "__main__":
    #runs the app
    FlaskUI(
        app=app,
        socketio=socketio,
        server="flask_socketio",
        port=5003,
        width=800,
        height=800,
    ).run()
    


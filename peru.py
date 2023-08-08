#!/bin/python
import re
from llama_cpp import Llama
from flask import Flask, render_template, request, jsonify

app = Flask(__name__,  static_folder='static')
llm = Llama(model_path="/Users/evanbarclay/Desktop/llama2/llama.cpp/models/7B/ggml-model-q4_0.bin")

def chat(text):
    text = llm(text, max_tokens=512,)
    return text

def format(text):
    text = str(text)
    print(text)
    text = "Q:" + text + "? A:"
    text = text[212:-137]
    text = (re.sub(r'\\.',lambda x:{'\\n':'\n','\\t':'\t'}.get(x[0],x[0]),text))
    return text

def generate(text):
    text = chat(text)
    text = format(text)
    return text

@app.route('/', methods=['GET'])
def peru0(name=None):
    return render_template('index.html', name=name)

@app.route('/', methods=['POST','GET'])
def peru1():
    text = request.form['textbox']
    text = generate(text)   
    return render_template('index.html', out=text)

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5003)
#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor 
import random

app = Flask(__name__)

names = open('names.txt', 'r')

@app.route('/')
def index():
    return random.choice(names)

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run(host='0.0.0.0')

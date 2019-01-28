#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor 
import random

app = Flask(__name__)

f = open('names.txt', 'r')
names = f.readlines()
f.close()

@app.route('/')
def index():
    return random.choice(names).strip()

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run(host='0.0.0.0', port=8080)

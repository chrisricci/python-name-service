#!flask/bin/python
from flask import Flask
from flask_prometheus import monitor 
from opentracing.ext import tags
from opentracing.propagation import Format
import random

app = Flask(__name__)

f = open('names.txt', 'r')
names = f.readlines()
f.close()

@app.route('/')
def index():
    tracer = init_tracer('name-service')
    getName(tracer)

def getName(tracer):
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_active_span('get-name', child_of=span_ctx, tags=span_tags):
        return random.choice(names).strip()

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run(host='0.0.0.0', port=8080)

#!flask/bin/python
from flask import Flask, request
from flask_prometheus import monitor
from opentracing.ext import tags
from opentracing.propagation import Format
from jaeger_client import Config
import random
import logging
import sys

app = Flask(__name__)
def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
    )
    return config.initialize_tracer()

tracer = init_tracer('greeting-service')

f = open('names.txt', 'r')
names = f.readlines()
f.close()

@app.route('/')
def index():
    span_ctx = tracer.extract(Format.HTTP_HEADERS, request.headers)
    span_tags = {tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER}
    with tracer.start_span('get-name', child_of=span_ctx, tags=span_tags):
        name = random.choice(names).strip()
        app.logger.debug('NAME: ' + name)
        return name

if __name__ == '__main__':
    monitor(app, port=8000)
    app.run(host='0.0.0.0', port=8080)

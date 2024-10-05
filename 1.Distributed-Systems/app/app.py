import logging

from flask import Flask

from routing.routing import Routing

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

Routing.init(app)

if __name__ == '__main__':
    app.run(port=5000)
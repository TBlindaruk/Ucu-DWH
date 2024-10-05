import logging

from flask import Flask

from action.messages import create, get

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

## TODO: I neet move it to routiing

messages = []

app.add_url_rule('/messages', 'create', create.create_action, methods=['POST'])
app.add_url_rule('/messages', 'get', get.get_list_action, methods=['GET'])

if __name__ == '__main__':
    app.run(port=5000)
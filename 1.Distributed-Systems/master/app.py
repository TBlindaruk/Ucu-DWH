import logging

from flask import Flask

from action.messages import create, get

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

## TODO: I neet move it to routiing

messages = []

app.add_url_rule('/messages', 'create', lambda : create.create_action(messages), methods=['POST'])
app.add_url_rule('/messages', 'get', lambda : get.get_list_action(messages), methods=['GET'])

if __name__ == '__main__':
    app.run(port=5000)
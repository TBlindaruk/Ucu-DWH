import logging
from time import sleep
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


messages = []

## it should with some internal auth, but it is not scope of that task
## actually it will be better to create as 1 app with different type, but let it be like this
@app.post('/internal/messages')
def create():
    data = request.json
    logger.info(f"SLAVE: initiate save data: {data}")
    messages.append(data)

    sleep(int(os.getenv("SLEEP")))
    logger.info(f"SLAVE: finished save data: {data}")

    return [], 201

@app.get('/messages')
def get_list():
    return jsonify({ "data": messages}), 200

if __name__ == '__main__':
    app.run(port=5001)
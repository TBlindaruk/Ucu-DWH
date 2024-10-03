import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from flask import Flask, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

messages = []

executor = ThreadPoolExecutor()

def replicate_message(message, replica_url):
    try:
        logger.info(f"MASTER: send message from master. message: {message} , replica: {replica_url}")

        response = requests.post(replica_url + '/internal/messages', json=message)

        if response.status_code == 201:
            logger.info(f"MASTER: success send message: {message} to {replica_url}")
            return True
        else:
            logger.info(f"MASTER: un success send message: {message} to {replica_url}")
            return False

    except Exception as e:
        logger.info(f"MASTER: error when send message: {message['text']} to {replica_url}. ERROR: {e}")
        return False

@app.post('/messages')
def create():
    data = request.json
    messages.append(data)
    count_of_replica_concern = int(os.getenv('CONCERN')) - 1

    futures = []
    success_counter = 0

    replica_env_vars = {key: value for key, value in os.environ.items() if key.startswith("REPLICA_HOST")}


    logger.info(f"MASTER: replica list: {replica_env_vars}")

    for env_key, replica_url in replica_env_vars.items():
        logger.info(f"MASTER: start for for: {replica_url}")
        future = executor.submit(replicate_message, data, replica_url)
        futures.append(future)

    if count_of_replica_concern <= 0:
        return [], 201

    for future in as_completed(futures):
        result = future.result()
        if result == True:
            success_counter += 1

        if success_counter >= count_of_replica_concern:
            return [], 201

    logger.info(f"MASTER: all responses is get")

    return [], 201

@app.get('/messages')
def get_list():
    return jsonify({ "data": messages}), 200

if __name__ == '__main__':
    app.run(port=5000)
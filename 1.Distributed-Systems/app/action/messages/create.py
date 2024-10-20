import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from flask import request

from request_dto.messages import CreateMessageRequestData
from service import MessageStoreSingleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor()

def create_action():
    data = CreateMessageRequestData.get_data()

    position = MessageStoreSingleton().append(data)
    count_of_replica_concern = CreateMessageRequestData.count_of_replica_concern()

    futures = []
    success_counter = 0

    replica_env_vars = {key: value for key, value in os.environ.items() if key.startswith("REPLICA_HOST")}

    logger.info(f"MASTER: replica list: {replica_env_vars}")

    for env_key, replica_url in replica_env_vars.items():
        logger.info(f"MASTER: start for for: {replica_url}")
        future = executor.submit(replicate_message, data, replica_url, position)
        futures.append(future)

    if count_of_replica_concern <= 0:
        return [], 201

    for future in as_completed(futures):
        result = future.result()
        if result:
            success_counter += 1

        if success_counter >= count_of_replica_concern:
            return [], 201

    logger.info(f"MASTER: all responses is get")

    return [], 201

def replicate_message(message, replica_url: str, position: int):
    try:
        logger.info(f"MASTER: send message from master. message: {message} , replica: {replica_url}")

        response = requests.post(replica_url + '/internal/messages/' + str(position), json=message)

        if response.status_code == 201:
            logger.info(f"MASTER: success send message: {message} to {replica_url}")
            return True
        else:
            logger.info(f"MASTER: un success send message: {message} to {replica_url}")
            return False

    except Exception as e:
        logger.info(f"MASTER: error when send message: {message['text']} to {replica_url}. ERROR: {e}")
        return False

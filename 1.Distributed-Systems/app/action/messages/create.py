import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from request_dto.messages import CreateMessageRequestData
from service import MessageStoreSingleton, UnsentMessageStoreSingleton

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
        future = executor.submit(replicate_message, data, replica_url, position, 5)
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

def replicate_message(message, replica_url: str, position: int, retry_count:int, run_unsent = True):
    try:
        logger.info(f"MASTER: send message from master. message: {message} , replica: {replica_url}")

        response = requests.post(replica_url + '/internal/messages/' + str(position), json=message)

        if response.status_code == 201:
            logger.info(f"MASTER: success send message: {message} to {replica_url}")
            if run_unsent:
                process_unsent_message(replica_url)

            return True
        else:
            logger.info(f"MASTER: unsuccessful send message: {message} to {replica_url}")
            if retry_count > 0:
                delay = (2 ** (5 - retry_count))
                logger.info(f"MASTER: retrying in {delay} seconds...")
                time.sleep(delay)
                return replicate_message(message, replica_url, position, retry_count - 1)

            UnsentMessageStoreSingleton().insert_into_replica_with_position(replica_url, position, message)
            return False

    except Exception as e:
        logger.info(f"MASTER: error when sending message: {message['text']} to {replica_url}. ERROR: {e}")

        if retry_count > 0:
            delay = (2 ** (5 - retry_count))
            logger.info(f"MASTER: retrying in {delay} seconds...")
            time.sleep(delay)
            return replicate_message(message, replica_url, position, retry_count - 1)

        UnsentMessageStoreSingleton().insert_into_replica_with_position(replica_url, position, message)
        return False

def process_unsent_message(replica_url: str):
    messages = UnsentMessageStoreSingleton().get_by_replica_name(replica_url)

    futures = []
    keys_to_remove = []

    for position, message  in messages.items():
        logger.info(f"MASTER: REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE {position} to {message}.")
        future = executor.submit(replicate_message, message, replica_url, position, 5, False)
        futures.append(future)

        for future in as_completed(futures):
            result = future.result()
            if result:
                keys_to_remove.append(position)

    for key_to_remove in keys_to_remove:
        UnsentMessageStoreSingleton().delete_by_replica_name_and_position(replica_url, key_to_remove)

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from api.data.messages import CreateMessageRequestData
from service import MessageStoreSingleton
from service.master.replica.message_manager import replicate_message
from service.quorum.manager import is_quorum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

executor = ThreadPoolExecutor()

def create_action():
    if not is_quorum():
        return ["We have a problem with replicas"], 400

    data = CreateMessageRequestData.get_data()

    position = MessageStoreSingleton().append(data)
    count_of_replica_concern = CreateMessageRequestData.count_of_replica_concern()

    futures = []
    success_counter = 0

    replica_env_vars = {key: value for key, value in os.environ.items() if key.startswith("REPLICA_HOST")}

    for env_key, replica_url in replica_env_vars.items():
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

    return [], 201

import logging
import time

import requests

from service import UnsentMessageStoreSingleton
from service.healthy import secondaries_status
from service.healthy.status_dist import HealthStatus

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def replicate_message(message, replica_url: str, position: int, retry_count:int):
    try:
        if secondaries_status[replica_url]['status'] != HealthStatus.HEALTHY.value:

            logger.info(f'MASTER: we do not use retry and to not try to send requests, since status is not HEALTHY {replica_url} . {retry_count}')

            UnsentMessageStoreSingleton().insert_into_replica_with_position(replica_url, position, message)

            return False

        logger.info(f'MASTER: TRY TO SEND {replica_url} . {retry_count}')
        response = requests.post(replica_url + '/internal/messages/' + str(position), json=message)

        if response.status_code == 201:
            return True
        else:
            if retry_count > 0:
                delay = (2 ** (5 - retry_count))
                time.sleep(delay)
                return replicate_message(message, replica_url, position, retry_count - 1)

            UnsentMessageStoreSingleton().insert_into_replica_with_position(replica_url, position, message)

            return False

    except Exception as e:
        if retry_count > 0:
            delay = (2 ** (5 - retry_count))
            time.sleep(delay)

            logger.info(f'MASTER: retry number {5- retry_count} to {replica_url}')

            return replicate_message(message, replica_url, position, retry_count - 1)

        UnsentMessageStoreSingleton().insert_into_replica_with_position(replica_url, position, message)

        logger.info(f"MASTER: replica ERROR: {e}")

        return False

import logging
import os
from time import sleep

from flask import request

from service import MessageStoreSingleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_action():
    data = request.json
    logger.info(f"SLAVE: initiate save data: {data}")
    MessageStoreSingleton().add_message(data)

    sleep(int(os.getenv("SLEEP")))
    logger.info(f"SLAVE: finished save data: {data}")

    return [], 201
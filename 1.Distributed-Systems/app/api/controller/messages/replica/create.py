import logging
import os
import random
from time import sleep

from flask import request

from service import MessageStoreSingleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_action(position: int):
    data = request.json

    my_list = [1, 10, 30,  50, 100]
    random_element = random.choice(my_list)

    logger.info(f"SLAVE: initiate save data: {data}. SLEEP: {random_element}")

    sleep(random_element)

    MessageStoreSingleton().insert_with_order(position, data)

    logger.info(f"SLAVE: finished save data: {data}")

    return [], 201
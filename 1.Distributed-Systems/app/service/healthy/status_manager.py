import time

import requests

from config import GeneralConfig
from service.healthy.status_dist import HealthStatus

secondaries = GeneralConfig.get_replicas()
max_attempts = 3
check_interval = 5

secondaries_status = {secondary_value: {"status": HealthStatus.HEALTHY.value, "failed_attempts": 0} for secondary_key, secondary_value in secondaries.items()}

def update_status(secondary):
    secondaries_status[secondary]["failed_attempts"] += 1
    if secondaries_status[secondary]["failed_attempts"] < max_attempts:
        secondaries_status[secondary]["status"] = HealthStatus.SUSPECTED.value
    else:
        secondaries_status[secondary]["status"] = HealthStatus.UNHEALTHY.value


def check_secondary(secondary):
    try:
        response = requests.get(f"{secondary}/internal/health", timeout=100)
        if response.status_code == 200:
            secondaries_status[secondary]["status"] = HealthStatus.HEALTHY.value
            secondaries_status[secondary]["failed_attempts"] = 0
        else:
            update_status(secondary)
    except requests.RequestException:
        update_status(secondary)

def heartbeat():
    while True:
        for secondary_key, secondary_value in secondaries.items():
            check_secondary(secondary_value)
        time.sleep(check_interval)


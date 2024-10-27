import logging
import math

from service.healthy import secondaries_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from service.healthy.status_dist import HealthStatus

def is_quorum():
    quorum = math.ceil((len(secondaries_status) + 1) / 2)

    logger.info(f"QUORUM: {quorum}")

    healthy_secondaries = {
        key: value for key, value in secondaries_status.items()
        if value["status"] == HealthStatus.HEALTHY.value
    }

    if (len(healthy_secondaries) + 1) >= quorum:
        return True

    return False

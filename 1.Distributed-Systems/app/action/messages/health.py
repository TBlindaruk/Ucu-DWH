import time

from healthy import HealthStatus

# TODO: actually it it should be smartest way - check env. and so on, but it is out of that scope
def get_health():
    current_time = int(time.time())
    status = HealthStatus.HEALTHY.value

    if current_time % 3 == 2:
        status = HealthStatus.SUSPECTED.value
    elif current_time % 3 == 1:
        status = HealthStatus.UNHEALTHY.value
    return [status, ], 200
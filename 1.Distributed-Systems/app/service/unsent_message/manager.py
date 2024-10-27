from concurrent.futures import ThreadPoolExecutor, as_completed
import time

from config import GeneralConfig
from service import UnsentMessageStoreSingleton
from service.master.replica.message_manager import replicate_message

executor = ThreadPoolExecutor()

class UnsentMessageProcessor:

    @staticmethod
    def __process_unsent_message(replica_url: str):
        messages = UnsentMessageStoreSingleton().get_by_replica_name(replica_url)

        futures = []
        keys_to_remove = []

        for position, message  in list(messages.items()):
            future = executor.submit(replicate_message, message, replica_url, position, 5)
            futures.append(future)

            for future in as_completed(futures):
                result = future.result()
                if result:
                    keys_to_remove.append(position)

        for key_to_remove in keys_to_remove:
            UnsentMessageStoreSingleton().delete_by_replica_name_and_position(replica_url, key_to_remove)

    def process_unsent_messages(self):
        while True:
            for secondary_key, secondary_value in GeneralConfig.get_replicas().items():
                self.__process_unsent_message(secondary_value)
            time.sleep(3)

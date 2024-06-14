
from generated.person import Person
import pitica
import os
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s | %(message)s')

ROOT_DIR = os.path.join(os.path.dirname(__file__), "generated")

pitica.setup_persistance(ROOT_DIR,
                         host="localhost",
                         port=6060,
                         user="root",
                         password="lanuma",
                         database="pitica",
                         engine=pitica.PersistanceEngine.MYSQL)

pitica.setup_notifications(host="localhost",
                           port=6379,
                           id="ping"
                           engine=pitica.NotificationsEngine.REDIS_PS)

listener_id: int = 0


def callback(classname: str, data: dict):
    person: Person = Person.get_by_id(data['id'])
    if not person:
        return
    logger.info(f"Setting age to {person.get_name()} to 30")
    pitica.disable_listener(listener_id)
    person.set_age(30).update()
    time.sleep(1)
    id = pitica.enable_listener(listener_id)


id = pitica.add_listener(
    pitica.NotificationType.EDITION, set([Person]), callback=callback)

time.sleep(30)

pitica.remove_listener(id)

import os
import time
import pitica
from generated.person import Person
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
                           id="pong"
                           engine=pitica.NotificationsEngine.REDIS_PS)


listener_id: int = 0


def callback(classname: str, data: dict):
    if "id" not in data:
        logger.error(
            f"ID not in data for new notification of {classname}")
        return
    person: Person = Person.find_by_id(data['id'])
    if not person:
        return
    logger.info(f"Setting age to {classname} {person.get_name()} to 16")
    pitica.disable_listener(id)
    person.set_age(16).update()
    time.sleep(1)
    pitica.enable_listener(id)


listener_id = pitica.add_listener(
    pitica.NotificationType.EDITION, set([Person]), callback=callback)

tom: Person = Person().set_name("Tom").set_dni(
    "11111111111111111").set_age(30).create()
tom.set_age(16).update()

time.sleep(30)

pitica.remove_listener(id)
tom.delete()

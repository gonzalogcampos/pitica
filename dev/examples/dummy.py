import os
import time
import pitica
from generated.person import Person
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s | %(message)s')

ROOT_DIR = os.path.join(os.path.dirname(__file__), "generated")

id: int = 0


def callback(classname: str, data: dict):
    person: Person = Person.get_by_id(data['id'])
    if person:
        logger.info(f"Changed {classname} {person.get_name()} to {data}")


id = pitica.add_listener(
    pitica.NotificationType.EDITION, set([Person]), callback=callback)

tom: Person = Person().set_name("Tom").set_dni("1").set_age(30).create()
try:
    tom.set_age(16).update()
except Exception as err:
    logger.info(err)

time.sleep(2)
pitica.remove_listener(id)

try:
    tom.delete()
except Exception as err:
    logger.info(err)

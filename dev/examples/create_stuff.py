from generated.subject import Subject
from generated.teacher import Teacher
from generated.person import Person
from generated.student import Student
import os
import pitica
from pitica.filter import FilterOperator
import logging

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)8s] | %(message)s')

ROOT_DIR = os.path.join(os.path.dirname(__file__), "generated")

pitica.setup_persistance(ROOT_DIR,
                         host="localhost",
                         port=6060,
                         user="root",
                         password="lanuma",
                         database="pitica",
                         engine=pitica.PersistanceEngine.MYSQL)

# pitica.setup_notifications(host="localhost",
#                            port=6379,
#                            id="stuff"
#                            engine=pitica.NotificationsEngine.REDIS)

# Insert some data
subjects = [
    ["Programming 101"]
]

students = [
    ["Juan", "2", 24],
    ["Maria", "3", 30],
    ["Lucia", "4", 31],
    ["Carlos", "5", 32],
    ["Carlos", "45", 33],
    ["Clara", "6", 34]
]

teachers = [
    ["Gonzalo", "1", 40]
]


for subject in Subject.find_all():
    subject.delete()

for student in Student.find_all():
    student.delete()

for teacher in Teacher.find_all():
    teacher.delete()

for person in Person.find_all():
    person.delete()

for teacher in teachers:
    person: Person = Person().set_name(teacher[0]).set_dni(
        teacher[1]).set_age(teacher[2]).create()
    my_teacher: Teacher = Teacher().set_person(person).create()

for subject in subjects:
    my_subject: Subject = Subject().set_name(
        subject[0]).set_teacher(my_teacher).create()

for student in students:
    person = Person().set_name(student[0]).set_dni(
        student[1]).set_age(student[2]).create()
    my_student = Student().set_person(person).add_subject(my_subject).create()

person.set_age(34).update()

subject: Subject
student: Student
for subject in Subject.find_all():
    logger.info(f"Subject: {subject.get_name()}")
    logger.info(f"   Teacher: {subject.get_teacher().get_person().get_name()}")
    logger.info(f"   Students:")
    for student in subject.get_students():
        logger.info(f"      - {student.get_person().get_name()}")


logger.info("")
logger.info(
    f"Name of person with dni 1 is: {Person.find_by_dni('1').get_name()}")

logger.info("")
logger.info("People older than 32:")
for person in Person.find_by_age(32, filter_operator=FilterOperator.GREATER):
    logger.info(f"   - {person.get_name()}")


logger.info("")
logger.info("DNI of people called 'Carlos':")
for person in Person.find_by_name("Carlos", filter_operator=FilterOperator.EQUALS):
    logger.info(f"   - {person.get_dni()}")

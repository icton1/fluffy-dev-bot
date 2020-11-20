from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from telegrambot.database.models import Student, Base, Teacher


class Database:
    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(bind=engine)

    def add_student(self, student):
        self.session.add(student)
        self.session.commit()

    def add_teacher(self, teacher):
        self.session.add(teacher)
        self.session.commit()

    def get_students(self):
        return self.session.query(Student).all()

    def get_teachers(self):
        return self.session.query(Teacher).all()

    def get_students_by_chat_id(self, chat_id):
        return self.session.query(Student).filter(chat_id=chat_id)

    def get_students_by_chat_id(self, chat_id):
        return self.session.query(Teacher).filter(chat_id=chat_id)


db = Database('sqlite:///university.db')
test_s = Student(123, 'Egor', 'Platonov', 'Nikolaevich', 'Y2435')
test_t = Teacher(456, 'Denis', 'Legin', 'Anatolievich', 'Math')
print(db.get_teachers())

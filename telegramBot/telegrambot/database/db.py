from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from telegrambot.database.models import Student, Base, Teacher


class Database:
    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(bind=engine)

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get(self, obj):
        return self.session.query(obj).all()

    def get_students_by_chat_id(self, chat_id):
        return self.session.query(Student).filter(chat_id=chat_id)

    def get_students_by_chat_id(self, chat_id):
        return self.session.query(Teacher).filter(chat_id=chat_id)

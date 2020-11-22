from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from datetime import date

from telegrambot.database.models import Base, Quest, Student, Teacher


class Database:
    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(bind=engine)

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def get_table_details(self, obj):
        return self.session.query(obj).all()

    def get_students_by_chat_id(self, chat_id):
        return self.session.query(Student).filter(Student.user_id == chat_id).first()

    def get_teacher_by_chat_id(self, chat_id):
        return self.session.query(Teacher).filter(Teacher.user_id == chat_id).first()

    def get_quests_by_deadline_after_current(self, chat_id):
        return self.session.query(Quest).filter(and_(Quest.deadline >= date.today(), Quest.student_id == chat_id)).all()

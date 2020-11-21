from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

from telegrambot.database.models import Base, Quest


class Database:
    def __init__(self, obj):
        engine = create_engine(obj, echo=False)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(bind=engine)

    def add(self, obj):
        self.session.add(obj)
        self.session.commit()

    def getTableDetails(self, obj):
        return self.session.query(obj).all()

    def get_students_or_teacher_by_chat_id(self, chat_id, obj):
        return self.session.query(obj).filter(chat_id=chat_id).first()

    def get_quests_by_deadline_after_current(self):
        return self.session.query(Quest).filter(Quest.deadline >= date.today()).all()

from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    subject = Column(String(50), nullable=False)

    def __init__(self, user_id, name, surname, patronymic, subject):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.subject = subject

    def __repr__(self):
        return "Teacher(%s, '%s', '%s', '%s', '%s')" % (self.user_id, self.name, self.surname, self.patronymic,
                                                        self.subject)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    group = Column(String(10), nullable=False)

    def __init__(self, user_id, name, surname, patronymic, group):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.group = group

    def __repr__(self):
        return "Student(%s, '%s', '%s', '%s', '%s')" % (
            self.user_id, self.name, self.surname, self.patronymic, self.group)



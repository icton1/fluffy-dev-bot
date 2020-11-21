from sqlalchemy import Column, String, Integer, Text, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)

    def __init__(self, user_id, name, surname, patronymic):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic

    def __repr__(self):
        return "Teacher(%s, '%s', '%s', '%s')" % (self.user_id, self.name, self.surname, self.patronymic)


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=False)
    group = Column(String(10), nullable=False)
    status = Column(String(20), nullable=False)

    def __init__(self, user_id, name, surname, patronymic, group, status):
        self.user_id = user_id
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.group = group
        self.status = status

    def __repr__(self):
        return "Student(%s, '%s', '%s', '%s', '%s', '%s')" % (
            self.user_id, self.name, self.surname, self.patronymic, self.group, self.status)


class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    subject = Column(String(100), nullable=False)
    deadline = Column(Date)
    student_id = Column(Integer, ForeignKey("students.id"))

    def __init__(self, text, subject, deadline, student_id):
        self.text = text
        self.subject = subject
        self.deadline = deadline
        self.student_id = student_id

    def __repr__(self):
        return "Quest(%s, '%s', '%s', '%s')" % (self.text, self.subject, self.deadline, self.student_id)

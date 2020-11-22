from datetime import date

import telebot
from telegrambot.database.db import Database
from telegrambot.database.models import Teacher, Student, Quest
from sqlalchemy.exc import IntegrityError

access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token)

db = Database('sqlite:///university.db')

status = -1


@bot.message_handler(commands=["start"])
def default_test(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/registration')
    bot.send_message(message.from_user.id,
                     "Добро пожаловать, перед началом работы,\n"
                     "Пожалуйста, ознакомьтесь с функционалом.\n"
                     "Прежде всего вам необходимо зарегистрироваться",
                     reply_markup=user_markup)


@bot.message_handler(commands=['help'])
def handle_start(message):
    global status
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if status == 0:
        user_markup.row('/write_message')
        user_markup.row('/send_homework')
    else:
        user_markup.row('/deadline_check')
    bot.send_message(message.from_user.id, "Вам доступны следующие команды",
                     reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def first_try(message):
    if message.text == '/registration':
        students = db.get_table_details(Student)
        teachers = db.get_table_details(Teacher)
        for student in students:
            if student.user_id == message.chat.id:
                bot.send_message(message.chat.id, "Вы уже зарегистрированы")
                return
        for teacher in teachers:
            if teacher.user_id == message.chat.id:
                bot.send_message(message.chat.id, "Вы уже зарегистрированы")
                return
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "Преподаватель / Студент ")
        bot.register_next_step_handler(send, go_next)
    elif message.text == '/write_message':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Завтра пар не будет (сообщение группам)")
        bot.register_next_step_handler(send, message_to_groups)
    elif message.text == '/send_homework':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Математика\n"
                                                 "ЛР10. Методичка. (сообщение группам)\n"
                                                 "2020-11-22 (дата сдачи)\n")
        bot.register_next_step_handler(send, homework)
    elif message.text == '/my_deadlines':
        s_id = db.get_students_by_chat_id(message.chat.id)
        list_deadline = db.get_quests_by_deadline_after_current(s_id.id)
        for deadline in list_deadline:
            bot.send_message(message.chat.id, deadline.text)


def registration(message):
    try:
        global status
        surname, name, patronymic, subject = message.text.split('\n')
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректные данные, повторите попытку')
        message.text = '/registration'
        first_try(message)
        return
    try:
        if status == 0:
            db.add(Teacher(message.chat.id, name, surname, patronymic))
        else:
            db.add(Student(message.chat.id, name, surname, patronymic, subject, status))
    except IntegrityError:
        return bot.send_message(message.chat.id, "Вы уже зарегистрированы!\n Нажмите /help, чтобы продолжить ")
    bot.send_message(message.chat.id,
                     "{name} {patronymic}, Вы успешно зарегестрированы!\n Нажмите /help, чтобы продолжить".format(
                         name=name,
                         patronymic=patronymic))


def message_to_groups(message):
    try:
        groups, mess = message.text.split('\n')
    except ValueError:
        bot.send_message(message.chat.id, "Некорректные данные, возврат в меню")
        return
    groups = groups.split()
    students = db.get_table_details(Student)
    for group in groups:
        for student in students:
            if student.group == group:
                bot.send_message(student.user_id, mess)
    bot.send_message(message.chat.id, "Сообщения отправлены!")


def go_next(message):
    global status
    if message.text.lower() == 'преподаватель':
        sent = bot.send_message(message.chat.id, "Иванов (фамилия)\n"
                                                 "Иван (имя) \n"
                                                 "Иванович (отчество)\n"
                                                 "Математика (предмет)")
        status = 0
        bot.register_next_step_handler(sent, registration)

    elif message.text.lower() == 'студент':
        sent = bot.send_message(message.chat.id, "Иванов (фамилия)\n"
                                                 "Иван (имя) \n"
                                                 "Иванович (отчество)\n"
                                                 "k3240 (Учебная группа)")
        status = 1
        bot.register_next_step_handler(sent, registration)

    else:
        bot.send_message(message.chat.id, 'Проверьте правильность введённых данных')


def homework(message):
    try:
        groups, subject, text, deadline = message.text.split("\n")
    except ValueError:
        bot.send_message(message.chat.id, "Некорректные данные, возврат в меню")
        return
    groups = groups.split()
    students = db.get_table_details(Student)
    deadline = deadline.split("-")
    for group in groups:
        for student in students:
            if student.group == group:
                bot.send_message(student.user_id, message.text)
                try:
                    db.add(Quest(text, subject, date(int(deadline[0]), int(deadline[1]), int(deadline[2])), student.id))
                except:
                    return


if __name__ == '__main__':
    bot.polling(none_stop=True)

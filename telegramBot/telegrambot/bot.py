from datetime import date

import telebot
from sqlalchemy.exc import IntegrityError

from telegrambot.database.db import Database
from telegrambot.database.models import Teacher, Student, Quest

access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token, threaded=False)

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
    if status == -1:
        update_status(message)
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    if status == 0:
        user_markup.row('/write_message')
        user_markup.row('/send_homework')
    else:
        user_markup.row('/deadline')
    bot.send_message(message.from_user.id, "Вам доступны следующие команды",
                     reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def first_try(message):
    global status
    update_status(message)
    if message.text == '/registration':
        if status != -1:
            bot.send_message(message.chat.id, "Вы уже зарегистрированы")
            return
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "Преподаватель / Студент ")
        bot.register_next_step_handler(send, go_next)
    elif message.text == '/write_message' and status == 0:
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Завтра пар не будет (сообщение группам)")
        bot.register_next_step_handler(send, message_to_groups)
    elif message.text == '/send_homework' and status == 0:
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Математика\n"
                                                 "ЛР10. Методичка. (сообщение группам)\n"
                                                 "2020-11-22 (дата сдачи (гггг-мм-дд))")
        bot.register_next_step_handler(send, homework)
    elif message.text == '/deadline' and status == 1:
        s_id = db.get_students_by_chat_id(message.chat.id)
        list_deadline = db.get_quests_by_deadline_after_current(s_id.id)
        if not list_deadline:
            bot.send_message(message.chat.id, "Заданий на последущие дни нет - проведите свободное время с умом.")
        for deadline in list_deadline:
            bot.send_message(message.chat.id, deadline.subject + "\n" + deadline.text + "\n" +
                             str(deadline.deadline))
    else:
        bot.send_message(message.chat.id, "Введена неверная команда, нажмите /help.")


def registration(message):
    try:
        global status
        if status == 0:
            surname, name, patronymic = message.text.split('\n')
        else:
            surname, name, patronymic, subject = message.text.split('\n')
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректные данные, повторите попытку')
        message.text = '/registration'
        status = -1
        first_try(message)
        return
    try:
        if status == 0:
            db.add(Teacher(message.chat.id, name, surname, patronymic))
        else:
            db.add(Student(message.chat.id, name, surname, patronymic, subject, status))
    except IntegrityError:
        return bot.send_message(message.chat.id, "Вы уже зарегистрированы!\nНажмите /help, чтобы продолжить ")
    bot.send_message(message.chat.id,
                     "{name} {patronymic}, Вы успешно зарегестрированы!\nНажмите /help, чтобы продолжить".format(
                         name=name,
                         patronymic=patronymic))


def message_to_groups(message):
    try:
        groups, mess = message.text.split('\n')
        teacher = db.get_teacher_by_chat_id(message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, "Некорректные данные, возврат в меню")
        return
    groups = groups.split()
    students = db.get_table_details(Student)
    for group in groups:
        for student in students:
            if student.group == group:
                bot.send_message(student.user_id, teacher.surname + " " + teacher.name + " " +
                                 teacher.patronymic + "\n\n" + mess)
    bot.send_message(message.chat.id, "Сообщения отправлены!")


def go_next(message):
    global status
    if message.text.lower() == 'преподаватель':
        sent = bot.send_message(message.chat.id, "Иванов (фамилия)\n"
                                                 "Иван (имя) \n"
                                                 "Иванович (отчество)")
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
        message.text = '/registration'
        first_try(message)


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
    bot.send_message(message.chat.id, "Сообщения отправлены!")


def update_status(message):
    global status
    students = db.get_table_details(Student)
    teachers = db.get_table_details(Teacher)
    for student in students:
        if student.user_id == message.chat.id:
            status = 1
            break
    if status != -1:
        return
    for teacher in teachers:
        if teacher.user_id == message.chat.id:
            status = 0
            break


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            bot.stop_polling()

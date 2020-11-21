import types
import telebot
from telebot import types
import telegrambot.first_func as frst
from telegrambot.database.db import Database
from telegrambot.database.models import Teacher, Student

access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token)


db = Database('sqlite:///university.db')


@bot.message_handler(content_types=['text'])
def first_try(message):
    if message.text == '/start':
        send = bot.send_message(message.chat.id, "Введите пожалуйста свои данные:\nИмя\n"
                                                 "Фамилия\n"
                                                 "Отчество\n"
                                                 "Предмет")
        bot.register_next_step_handler(send, registration)
    elif message.text == '/write_message':
        send = bot.send_message(message.chat.id, "Группы + Сообщение")
        bot.register_next_step_handler(send, message_to_groups)

    elif message.text == 'Дальше':
        start = ["Выберите пожалуйста функционал, которым хотите воспользоваться:"]
        bot.send_message(message.chat.id, start)
    else:
        bot.send_message(message.chat.id, db.get_students() + db.get_teachers())


"""
    elif message.text == '1':
        frst.first_f()
        ending_alert = "Если хотите продолжить, напишите 'Дальше'"
        bot.send_message(message.chat.id, ending_alert)

    else:
        return None
"""


def registration(message):
    status, name, surname, patronymic, subject = message.text.split()
    if status == 0:
        db.add_teacher(Teacher(message.chat.id, name, surname, patronymic, subject))
    else:
        db.add_student(Student(message.chat.id, name, surname, patronymic, subject))
    bot.send_message(message.chat.id, "{name} {patronymic}, Вы успешно зарегестрированы!".format(name=name,
                                                                                                 patronymic=patronymic))
    print(db.get_teachers())


def message_to_groups(message):
    group, mess = message.text.split()
    students = db.get_students()
    for student in students:
        if student.group == group:
            bot.send_message(student.user_id, mess)
    bot.send_message(message.chat.id, "Message deployed!")



@bot.message_handler(content_types=['voice'])
def kruto(message):
    kruto2 = "Пошел нахуй с аудио"
    bot.send_message(message.chat.id, kruto2)


if __name__ == '__main__':
    bot.polling(none_stop=True)

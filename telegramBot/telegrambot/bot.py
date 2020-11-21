import telebot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton
from telegrambot.database.db import Database
from telegrambot.database.models import Teacher, Student

access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token)

db = Database('sqlite:///university.db')


@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/write_message', '/main_quest', '/deadline_check')
    user_markup.row('/registration')
    bot.send_message(message.from_user.id,
                     "Добро пожаловать, перед началом работы,\n"
                     "Пожалуйста, ознакомьтесь с функционалом.\n"
                     "Прежде всего вам необходимо зарегистрироваться",
                     reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def first_try(message):
    if message.text == '/registration':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "Иванович (фамилия)\n"
                                                 "Иван (имя)\n"
                                                 "Иванов (отчество)\n"
                                                 "Математика (предмет)")
        bot.register_next_step_handler(send, registration)
    elif message.text == '/write_message':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Завтра пар не будет (сообщение группам)")
        bot.register_next_step_handler(send, message_to_groups)


def registration(message):
    try:
        status, surname, name, patronymic, subject = message.text.split('\n')
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректные данные, повторите попытку')
        message.text = '/start'
        first_try(message)
        return
    if status == 0:
        db.add(Teacher(message.chat.id, name, surname, patronymic, subject))
    else:
        db.add(Student(message.chat.id, name, surname, patronymic, subject))
    bot.send_message(message.chat.id, "{name} {patronymic}, Вы успешно зарегестрированы!".format(name=name,
                                                                                                 patronymic=patronymic))


def message_to_groups(message):
    try:
        groups, mess = message.text.split('\n')
    except ValueError:
        bot.send_message(message.chat.id, "Некорректные данные, возврат в меню")
        return
    groups = groups.split()
    students = db.get(Student)
    for group in groups:
        for student in students:
            if student.group == group:
                bot.send_message(student.user_id, mess)
    bot.send_message(message.chat.id, "Сообщения отправлены!")


if __name__ == '__main__':
    bot.polling(none_stop=True)

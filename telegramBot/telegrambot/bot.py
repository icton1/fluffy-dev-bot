import telebot
from telegrambot.database.db import Database
from telegrambot.database.models import Teacher, Student
from sqlalchemy.exc import IntegrityError

access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token)

db = Database('sqlite:///university.db')


@bot.message_handler(commands=["start"])
def default_test(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text="Авторизироваться через ИСУ",
                                            url="https://isu.ifmo.ru/pls/apex/f?p=2143:LOGIN:106933509959320")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Авторизируйся перед тем, как начать", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('/write_message')
    user_markup.row('/main_quest', '/deadline_check')
    bot.send_message(message.from_user.id,
                     "Добро пожаловать, перед началом работы,\n"
                     "Пожалуйста, ознакомьтесь с функционалом.\n"
                     "Прежде всего вам необходимо зарегистрироваться",
                     reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def first_try(message):
    if message.text == '/registration':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "Преподаватель / Студент ")
        bot.register_next_step_handler(send, go_next)
    elif message.text == '/write_message':
        send = bot.send_message(message.chat.id, "Введите данные в следующем формате:\n"
                                                 "K1234 K3412 (группы)\n"
                                                 "Завтра пар не будет (сообщение группам)")
        bot.register_next_step_handler(send, message_to_groups)


def registration(status, message):
    try:
        surname, name, patronymic, subject = message.text.split('\n')
        if (status == 'преподаватель') or (status == 'Преподаватель'):
            status = 0
        elif (status == 'студент') or (status == 'Студент'):
            status = 1
        else:
            bot.send_message(message.chat.id, 'Проверьте правильность введённых данных')
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректные данные, повторите попытку')
        message.text = '/registration'
        first_try(message)
        return
    try:
        if status == 0:
            db.add(Teacher(message.chat.id, name, surname, patronymic, subject))
        else:
            db.add(Student(message.chat.id, name, surname, patronymic, subject))
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
    students = db.get(Student)
    for group in groups:
        for student in students:
            if student.group == group:
                bot.send_message(student.user_id, mess)
    bot.send_message(message.chat.id, "Сообщения отправлены!")


def go_next(message):
    if (message.text == 'преподаватель') or (message.text == 'Преподаватель'):
        sent = bot.send_message(message.chat.id, "Иванов (фамилия)\n"
                                                 "Иван (имя) \n"
                                                 "Иванович (отчество)\n"
                                                 "Математика (предмет)")
        stat = 0
        bot.register_next_step_handler(sent, registration(stat, message.text))

    elif (message.text == 'студент') or (message.text == 'Студент'):
        sent = bot.send_message(message.chat.id, "Иванович (фамилия)\n"
                                                 "Иван (имя) \n"
                                                 "Иванов (отчество)\n"
                                                 "k3240 (Учебная группа)")
        stat = 1
        bot.register_next_step_handler(sent, registration(stat, message.text))

    else:
        bot.send_message(message.text.id, 'Проверьте правильность введённых данных')


if __name__ == '__main__':
    bot.polling(none_stop=True)

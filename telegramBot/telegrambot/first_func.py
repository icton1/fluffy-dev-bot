from typing import List, Tuple

from pygame.tests.ftfont_test import obj

from telegramBot.telegrambot import bot


def first_f():
    rules = "Если хотите оповестить студентов, пожалуйста напишите сообщение в следующей форме: Номер группы, " \
            "название предмета, текст оповещения "
    bot.send_message(message.chat.id, rules)
    group, obj, text = form()
    # Тут добавление в базу данных и отправка юзерам будет отдельной функцией
    return bot.send_message(message.chat.id)


def form():
    # Объяснение формы

    association = "{group}, {obj}, {text}".format(
        group=group,
        obj=obj,
        text=text
    )

    return association

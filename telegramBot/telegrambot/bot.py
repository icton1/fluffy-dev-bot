import telebot
import telegrambot.first_func as frst


access_token = "1489218543:AAGKxQNnAjHPLyc3LTYlk4adYWZKEj91NXE"
bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def first_try(message):
    if message.text == 'Дальше':
        start = ["Выберите пожалуйста функционал, которым хотите воспользоваться:"]
        bot.send_message(message.chat.id, start)
    elif message.text == '1':
        frst.first_f()
        ending_alert = "Если хотите продолжить, напишите 'Дальше'"
        bot.send_message(message.chat.id, ending_alert)

    else:
        return None


if __name__ == '__main__':
    bot.polling(none_stop=True)

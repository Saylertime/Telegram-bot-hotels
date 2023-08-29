import os
from telebot.types import Message
from loader import bot

@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """ Вызывается, когда пользователь без состояния вводит несуществующую команду """
    
    bot.reply_to(
        message, f"Такой команды нет: {message.text}\n"
                 f"Нажмите /start, чтобы посмотреть весь список команд"
    )

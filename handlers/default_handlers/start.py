from loader import bot
from telebot.types import Message

@bot.message_handler(commands=['start'])
def start_message(message: Message) -> None:
    """ Выдает стартовое сообщение со всеми доступными командами """

    msg = f"Привет, {message.from_user.first_name}! Ищи отель в любом городе.\n\n" \
          f"/low — показать самый дешевый отель\n\n" \
          f"/high — показать самый дорогой отель\n\n" \
          f"/custom — найти несколько отелей по критериям: дате, цене и количеству фото\n\n" \
          f"/history — посмотреть всю историю своих запросов"

    bot.send_message(message.chat.id, msg)

from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['help'])
def help(message: Message) -> None:
    """ Дает информацию по всем остальным командам """

    msg = f"/low — показать самый дешевый отель города\n\n" \
          f"/high — показать самый дорогой отель города\n\n" \
          f"/custom — найти несколько отелей по критериям: дате, цене и количеству фото\n\n" \
          f"/history — посмотреть всю историю своих запросов"

    bot.send_message(message.from_user.id, msg)

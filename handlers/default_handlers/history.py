from loader import bot
from db_maker import Person, Hotel
from telebot.types import Message

@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    """ Показываем историю поиска из базы данных """

    persons = Person.select().where(Person.username == message.from_user.username)

    history_messages = []
    for person in persons:
        hotels = Hotel.select().where(Hotel.owner == person)
        for hotel in hotels:
            created_at = person.created_at.strftime("%Y-%m-%d %H:%M")
            message_text = f"Время запроса: {created_at}\n" \
                           f"Команда: {person.command}\n" \
                           f"Город: {person.city}\n" \
                           f"Название отеля: {hotel.hotel_name}\n"
            history_messages.append(message_text)

    if history_messages:
        response_text = "\n".join(history_messages)
    else:
        response_text = "История не найдена"

    bot.send_message(message.from_user.id, response_text)
    
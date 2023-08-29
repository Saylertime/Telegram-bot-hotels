from endpoints.hotels import hotels
from keyboards.reply.create_markup import create_markup
from endpoints.images import images_download
from endpoints.property import property
from keyboards.reply.calendar import show_calendar
from states.overall import OverallState
from loader import bot
from endpoints.cities import cities, check_city
from utils.russian_cities import russian_cities
from utils.check_price import check_price
from db_maker import *
import datetime
import os
import time
from telebot.types import Message, InputMediaPhoto


@bot.message_handler(commands=['custom', 'high', 'low'])
def commands(message: Message) -> None:
    """ Ловит команды '/custom', '/high' и '/low' """

    bot.set_state(message.from_user.id, OverallState.city)
    with bot.retrieve_data(message.from_user.id) as data:
        data['command'] = message.text
        data['state'] = 'CustomState'
        data['minimum'] = 1
        data['maximum'] = 200
        data['date1'] = 0
        data['date2'] = 0
        data['hotels_count'] = 1

    if data['command'] == '/high':
        pricing = 'дорогой'
        data['date1'] = datetime.date.today()
        data['date2'] = data['date1'] + datetime.timedelta(days=1)
    elif data['command'] == '/low':
        pricing = 'дешевый'
        data['date1'] = datetime.date.today()
        data['date2'] = data['date1'] + datetime.timedelta(days=1)
    else:
        pricing = 'крутой'
    bot.send_message(message.from_user.id, f'Введите город (не российский). И мы покажем самый {pricing} отель в нем')

@bot.message_handler(state=OverallState.city)
def choose_city(message: Message) -> None:
    """ Проверяет корректность введенного города и отправляет пользователя дальше в зависимости от команды """

    if message.text.capitalize() in russian_cities:
        bot.send_message(message.from_user.id, 'Это российский город. Введите другой')
    elif not check_city(message.text):
        bot.send_message(message.from_user.id, 'Кажется, в названии города ошибка. '
                                                   'Либо его нет в списке. Попробуйте другой')
    else:
        with bot.retrieve_data(message.from_user.id) as data:
            data['city'] = message.text.capitalize()
    if data['command'] == '/high' or data['command'] == '/low':
        bot.set_state(message.from_user.id, OverallState.photo_count)
        photo_count(message)
    else:
        bot.set_state(message.from_user.id, OverallState.minimum)
        bot.send_message(message.from_user.id, "Теперь выберите даты для брони")
        show_calendar(bot, message.chat.id, 'заезда')

@bot.message_handler(state=OverallState.minimum)
def minimum(message: Message) -> None:
    """ Записывает минимальную стоимость в словарь и меняет состояние на следующее """

    if check_price(message.text):
        bot.send_message(message.chat.id, 'А теперь максимальную цена: ')
        bot.set_state(message.from_user.id, OverallState.maximum)
        with bot.retrieve_data(message.from_user.id) as data:
            data['minimum'] = message.text
    else:
        bot.send_message(message.chat.id, 'Значение должно быть без цифр и больше 0')

@bot.message_handler(state=OverallState.maximum)
def maximum(message: Message) -> None:
    """ Записывает максимальную стоимость и меняет состояние """

    if check_price(message.text):
        with bot.retrieve_data(message.from_user.id) as data:
            data['maximum'] = message.text
        bot.set_state(message.from_user.id, OverallState.photo_count)
        photo_count(message)
    else:
        bot.send_message(message.chat.id, 'Значение должно быть без цифр и больше 0')

@bot.message_handler(state=OverallState.photo_count)
def photo_count(message: Message) -> None:
    """ Предлагает выбрать количество фото """

    buttons = [('Без фото', '0'), ('1', '1'), ('2', '2')]
    markup = create_markup(buttons)
    bot.send_message(message.chat.id, "Выбери количество фото", reply_markup=markup)

@bot.message_handler(state=OverallState.hotels_count)
def hotels_count(message: Message) -> None:
    """ Предлагает выбрать количество отелей """

    buttons = [('1', 'Один'), ('2', 'Два'), ('3', 'Три')]
    markup = create_markup(buttons)
    bot.send_message(message.from_user.id, "Сколько отелей показать?", reply_markup=markup)


@bot.message_handler(state=OverallState.final)
def finals(call: Message) -> None:
    """ Записывает всю историю запроса в базу данных и выдает сообщение с отелями и фотографиями """

    with bot.retrieve_data(call.from_user.id) as data:
        date1 = datetime.datetime.strptime(str(data['date1']), '%Y-%m-%d')
        date2 = datetime.datetime.strptime(str(data['date2']), '%Y-%m-%d')
        minimum = data['minimum']
        maximum = data['maximum']
        p_count = int(data['photo'])
        difference = date2 - date1
        days = difference.days
        city_id = cities(data['city'])
        hotel_names_for_db = ''
        if data['command'] == '/low':
            sorting = 'PRICE_LOW_TO_HIGH'
        elif data['command'] == '/high':
            sorting = 'PRICE_HIGH_TO_LOW'
        else:
            sorting = 'PRICE_HIGHEST_FIRST'

        person = Person.create(username=call.from_user.username,
                               city=data['city'],
                               date1=data['date1'],
                               date2=data['date2'],
                               command=data['command'],
                               minimum=minimum,
                               maximum=maximum,
                               photo=p_count)

        for i_num in range(int(data['hotels_count'])):
            hotel_dict = hotels(city_id, i_num, sort=sorting,
                                minimum=int(minimum),
                                first_date=date1,
                                second_date=date2)
            hotel_name = hotel_dict['hotel_name']
            hotel_id = hotel_dict['hotel_id']
            hotel_price = hotel_dict['price_for_night']
            full_price = int(hotel_price[1:]) * int(days)
            hotel_distance = hotel_dict['distance_to_center']
            property_dict = property(hotel_id)
            star_rating = property_dict['rating']
            hotel_address = property_dict['address']

            msg = f"Город: {data['city']}\n" \
              f"Название отеля: {hotel_name}\n" \
              f"Адрес: {hotel_address}\n" \
              f"Количество звезд: {star_rating}\n" \
              f"Дата заезда: {data['date1']}\n" \
              f"Дата выезда: {data['date2']}\n" \
              f"От центра (км): {hotel_distance}\n"\
              f"Цена за ночь: {hotel_price}\n" \
              f"Цена за весь срок: ${full_price}\n\n"

            bot.send_message(call.message.chat.id, msg)

            if p_count == 2:
                images = images_download(hotel_id, int(data['photo']))
                print(images)
                media = [InputMediaPhoto(images[0]), InputMediaPhoto(images[1])]
                bot.send_media_group(call.message.chat.id, media)
            elif p_count == 1:
                image = images_download(hotel_id, int(data['photo']))
                print(image[0])
                bot.send_photo(call.message.chat.id, image[0])

            hotel_names_for_db += hotel_dict['hotel_name'] + " "

        Hotel.create(owner=person, hotel_name=hotel_names_for_db)
    bot.delete_state(call.from_user.id)



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call) -> None:
    """ Собираем колбэк-дату по количеству фотографий и отелей """

    if call.data in ['0', '1', '2'] and bot.get_state(call.from_user.id) == 'OverallState:photo_count':
        with bot.retrieve_data(call.from_user.id) as data:
            data['photo'] = call.data
        if data['command'] == '/high' or data['command'] == '/low':
            bot.set_state(call.from_user.id, OverallState.final)
            bot.send_message(call.message.chat.id, 'Подгружаю информацию...')
            finals(call)
        else:
            bot.set_state(call.from_user.id, OverallState.hotels_count)
            hotels_count(call)

    elif call.data in ['Один', 'Два', 'Три'] and bot.get_state(call.from_user.id) == 'OverallState:hotels_count':
        bot.send_message(call.message.chat.id, 'Подгружаю информацию...')
        with bot.retrieve_data(call.from_user.id) as data:
            if call.data == "Три":
                data['hotels_count'] = 3
            elif call.data == "Два":
                data['hotels_count'] = 2
            else:
                data['hotels_count'] = 1
        bot.set_state(call.from_user.id, OverallState.final)
        finals(call)

from telebot.handler_backends import State, StatesGroup

class OverallState(StatesGroup):
    """ Класс со всеми необходимыми состояниями """

    city = State()
    minimum = State()
    maximum = State()
    photo_count = State()
    hotels_count = State()
    final = State()
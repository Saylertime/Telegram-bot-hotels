import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("API_TOKEN")

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Посмотреть все команды"),
    ("low", "Самый дешевый отель города"),
    ("high", "Самый дорогой отель города"),
    ("custom", "Выбрать отель по критериям"),
    ("history", "Посмотреть историю запросов"),
)
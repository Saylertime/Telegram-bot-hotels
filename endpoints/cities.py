import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

def check_city(city):
	""" Проверяет, есть ли город в базе данных Hotels.com """

	try:
		url = "https://hotels4.p.rapidapi.com/locations/v3/search"
		querystring = {"q":city,"locale":"ru_RU","langid":"1033","siteid":"300000001"}
		headers = {
			"X-RapidAPI-Key": API_KEY,
			"X-RapidAPI-Host": API_HOST
		}
		response = requests.get(url, headers=headers, params=querystring, timeout=10)

		if response.status_code == 200:
			data = json.loads(response.text)
			city_id = data['sr'][1]['gaiaId']
			return True
	except:
		return False


def cities(city):
	""" Получает city_id для следующих запросов """

	url = "https://hotels4.p.rapidapi.com/locations/v3/search"

	querystring = {"q":city,"locale":"ru_RU","langid":"1033","siteid":"300000001"}

	headers = {
		"X-RapidAPI-Key": API_KEY,
		"X-RapidAPI-Host": API_HOST
	}

	response = requests.get(url, headers=headers, params=querystring, timeout=10)

	if response.status_code == 200:
		data = json.loads(response.text)
		city_id = data['sr'][1]['gaiaId']
		return city_id


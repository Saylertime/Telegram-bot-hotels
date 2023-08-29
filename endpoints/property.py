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

def property(property_id):
	""" Находит адрес отеля и его рейтинг"""

	url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"propertyId": property_id
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": API_KEY,
		"X-RapidAPI-Host": API_HOST
	}

	response = requests.post(url, json=payload, headers=headers, timeout=10)

	if response.status_code == 200:
		data = json.loads(response.text)

		property_dict = dict()
		property_dict['address'] = data['data']['propertyInfo']['summary']['location']['address']['addressLine']
		try:
			property_dict['rating'] = data['data']['propertyInfo']['summary']['overview']['propertyRating']['rating']
		except:
			property_dict['rating'] = 'Не определился :('

		return property_dict
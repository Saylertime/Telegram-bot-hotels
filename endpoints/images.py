import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

def images_download(hotel_id, quantity):
	""" Возвращает ссылки на фотографии отелей """

	album = []

	url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

	payload = {
		"currency": "RUB",
		"eapid": 1,
		"locale": "ru_RU",
		"siteId": 300000001,
		"propertyId": hotel_id
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": API_KEY,
		"X-RapidAPI-Host": API_HOST
	}

	response = requests.post(url, json=payload, headers=headers, timeout=10)
	print(response.status_code)

	if response.status_code == 200:
		data = json.loads(response.text)

		for i_num in range(quantity):
			image_url = data['data']['propertyInfo']['propertyGallery']['images'][i_num]['image']['url']
			album.append(image_url)

	return album

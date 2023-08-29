import requests
import json
import os
from dotenv import load_dotenv, find_dotenv

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

def hotels(city_id, quantity, sort, first_date, second_date, minimum=10, maximum=200):
    """ Возвращает словарь с названием отеля, его ID, ценой и расстоянием до центра """

    first_day = first_date.day
    first_month = first_date.month
    first_year = first_date.year
    second_day, second_month, second_year = second_date.day, second_date.month, second_date.year

    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "RUB",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": city_id},
        "checkInDate": {
            "day": first_day,
            "month": first_month,
            "year": first_year
        },
        "checkOutDate": {
            "day": second_day,
            "month": second_month,
            "year": second_year
        },
        "rooms": [
            {
                "adults": 2,
            }
        ],
        "resultsStartingIndex": 0,
        "resultsSize": 200,
        'sort': sort,
        'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY', "price": {
            "max": maximum,
            "min": minimum
        }}
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

        hotel_dict = dict()
        hotel_dict['hotel_name'] = data['data']['propertySearch']['properties'][quantity]['name']
        hotel_dict['hotel_id'] = data['data']['propertySearch']['properties'][quantity]['id']
        print(data['data']['propertySearch']['properties'][quantity]['price']['options'][0]['formattedDisplayPrice'])
        hotel_dict['price_for_night'] = data['data']['propertySearch']['properties'][quantity]['price']['options'][0]['formattedDisplayPrice']
        try:
            hotel_dict['distance_to_center'] = data['data']['propertySearch']['properties'][quantity]['destinationInfo']['distanceFromDestination']['value']
        except:
            hotel_dict['distance_to_center'] = "Не определилось"

        return hotel_dict
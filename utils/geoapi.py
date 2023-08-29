from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="myGeocoder")

def is_valid_city(city):
    try:
        location = geolocator.geocode(city)
        if location is None:
            return False
        else:
            return True
    except:
        return False


import re
from geopy.geocoders import Nominatim

import ssl

context = ssl._create_unverified_context()


def load_names(filename):
   with open(filename, 'r', encoding='utf-8') as file:
        cities = {line.strip().lower() for line in file if line.strip()}
        return cities

def extract_location(text, filename = 'Final_List.txt'):
    cities = load_names(filename)
    text_lower = text.lower()
    found_cities = []

    for city in cities:
        #match whole words only
        if re.search(r'\b' + re.escape(city) + r'\b', text_lower):
            found_cities.append(city)
    found_cities = [city for city in cities if city in text_lower]
    return found_cities



def get_coordinates(city_name):
    geolocator = Nominatim(user_agent = "city_coordinates_extractor", ssl_context=context)
    location = geolocator.geocode(city_name, timeout = 30)
    if location:
        return location.latitude, location.longitude
    else:
        return None

def main(*texts):
    for text in texts:
        print()
        print(f"Processing text: {text}")
        found_cities = extract_location(text)
        if found_cities:
            for city in found_cities:
                city_capitalized = city.title()
                print(f"City: {city_capitalized}")
                coordinates = get_coordinates(city_capitalized)
                if coordinates:
                    print(f"Coordinates: Latitude = {coordinates[0]}, Longitude = {coordinates[1]}")
                else:
                    print("Coordinates not found.")
        else:
            print("No city found in the text.")


# Change this to read from BlueSky Text Thread

# Read data from file
with open("data.txt", "r", encoding="utf-8") as file:
    #lines = [line.strip() for line in file.readlines() if line.strip()]  # Remove empty lines
    lines = file.read().splitlines()
# Call main function with the read data
main(*lines)

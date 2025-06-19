#!/usr/bin/env python
# coding: utf-8

# In[84]:


#-------INITIALIZE LIBRARIES AND WEBDRIVER-------

from selenium import webdriver
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from urllib3.exceptions import ReadTimeoutError
from fake_useragent import UserAgent
from zipch import ZipcodesDatabase
from geopy.distance import distance as geopy_distance
from geopy.distance import geodesic
import pyproj
from pyproj import Transformer
import rasterio
from rasterio.transform import from_origin
import json
import pandas as pd
import re
import pyautogui
import subprocess
import time
import requests
import os
import signal
import psutil
import random


# In[96]:


#Overall important Swiss cities/regions
swiss_hubs = {
    "Zurich": (47.3782, 8.5402),
    "Bern": (46.9491, 7.4384),
    "Geneva": (46.2106, 6.1429),
    "Basel": (47.5477, 7.5896),
    "Lausanne": (46.5171, 6.6291),
    "Winterthur": (47.5004, 8.7238),
    "Lucerne": (47.0505, 8.3102),
    "St. Gallen": (47.4231, 9.3695),
    "Lugano": (46.0051, 8.9469),
    "Biel": (47.1331, 7.2430),
    "Bienne": (47.1331, 7.2431),
    "Thun": (46.7550, 7.6300),
    "Bellinzona": (46.1951, 9.0290),
    "Köniz": (46.9248, 7.4152),
    "La Chaux-de-Fonds": (47.0988, 6.8251),
    "Chur": (46.8536, 9.5297),
    "Fribourg": (46.8033, 7.1514),
    "Schaffhausen": (47.6984, 8.6331),
    "Sion": (46.2276, 7.3595),
    "Neuchâtel": (46.9967, 6.9362),
    "Neuenburg": (46.9967, 6.9361),
    "Altstetten": (47.3917, 8.4885),
    "Lancy": (46.1874, 6.1262),
    "Baden": (47.4766, 8.3079),
    "Zug": (47.1736, 8.5155),
    "Emmen": (52.7904, 6.8996),
    "Olten": (47.3520, 7.9078),
    "Dübendorf": (47.4001, 8.6236),
    "Kriens": (47.0378, 8.2763),
    "Rapperswil-Jona": (47.2253, 8.8165),
    "Vernier": (46.2208, 6.0941),
    "Meyrin": (46.2225, 6.0765),
    "Wetzikon": (47.3181, 8.7927),
    "Baar": (47.1953, 8.5229),
    "Wil": (47.4625, 9.0410),
    "Wädenswil": (47.2294, 8.6752),
    "Aarau": (47.3914, 8.0517),
    "Riehen": (47.5834, 7.6522),
    "Wettingen": (47.4598, 8.3164),
    "Bülach": (47.5228, 8.5378),
    "Kloten": (47.4487, 8.5837),
    "Yverdon": (46.7816, 6.6409),
    "Frauenfeld": (47.5575, 8.8960),
    "Uster": (47.3510, 8.7176),
    "Dietikon": (47.4060, 8.4048),
    "Montreux": (46.0051, 8.9469),
    "Kreuzlingen": (47.6526, 9.1690),
    "Solothurn": (47.2046, 7.5430),
    "Appenzell": (47.3286, 9.4097),
    "Herisau": (47.3902, 9.2768),
    "Liestal": (47.4844, 7.7316),
    "Schwyz": (47.0269, 8.6321),
    "Glarus": (47.0398, 9.0714),
    "Delemont": (47.3621, 7.3500),
    "Stans": (46.9584, 8.3664),
    "Altdorf": (46.8760, 8.6318),
    "Sarnen": (46.8941, 8.2477),
    "Payerne": (46.8197, 6.9401),
    "Chiasso": (45.8322, 9.0320),
    "Sierre": (46.2923, 7.533),
}

#Cities with 20k+ population
swiss_big_cities = {
    "Zurich": (47.3782, 8.5402),
    "Bern": (46.9491, 7.4384),
    "Geneva": (46.2106, 6.1429),
    "Basel": (47.5477, 7.5896),
    "Lausanne": (46.5171, 6.6291),
    "Winterthur": (47.5004, 8.7238),
    "Lucerne": (47.0505, 8.3102),
    "St. Gallen": (47.4231, 9.3695),
    "Lugano": (46.0051, 8.9469),
    "Biel": (47.1331, 7.2430),
    "Thun": (46.7550, 7.6300),
    "Bellinzona": (46.1951, 9.0290),
    "Köniz": (46.9248, 7.4152),
    "La Chaux-de-Fonds": (47.0988, 6.8251),
    "Chur": (46.8536, 9.5297),
    "Fribourg": (46.8033, 7.1514),
    "Schaffhausen": (47.6984, 8.6331),
    "Sion": (46.2276, 7.3595),
    "Neuchâtel": (46.9967, 6.9362),
    "Lancy": (46.1874, 6.1262),
    "Zug": (47.1736, 8.5155),
    "Emmen": (52.7904, 6.8996),
    "Kriens": (47.0378, 8.2763),
    "Rapperswil-Jona": (47.2253, 8.8165),
    "Vernier": (46.2208, 6.0941),
    "Baar": (47.1953, 8.5229),
    "Riehen": (47.5834, 7.6522),
    "Yverdon": (46.7816, 6.6409),
    "Frauenfeld": (47.5575, 8.8960),
    "Uster": (47.3510, 8.7176),
    "Dietikon": (47.4060, 8.4048),
    "Montreux": (46.0051, 8.9469),
}

#Cities with 50k+ population
swiss_major_cities = {
    "Zurich": (47.3782, 8.5402),
    "Bern": (46.9491, 7.4384),
    "Geneva": (46.2106, 6.1429),
    "Basel": (47.5477, 7.5896),
    "Winterthur": (47.5003, 8.7238),
    "Lausanne": (46.5171, 6.6291),
    "Lucerne": (47.0505, 8.3102),
    "St. Gallen": (47.4231, 9.3695),
    "Lugano": (46.0051, 8.9469),
    "Biel": (47.1331, 7.2430),
}

# Add this at the top of your code
regional_importance = {
    "Zurich": 1.0,
    "Bern": 0.9,
    "Geneva": 0.9,
    "Basel": 0.9,
    "Winterthur": 0.8,
    "Lausanne": 0.8,
    "Lucerne": 0.8,
    "St. Gallen": 0.8,
    "Lugano": 0.7,
    "Biel": 0.6,
    # Default for unknown or rural areas
    "DEFAULT": 0.4
}


#Airports
swiss_major_airports = {
    "Zurich Flughafen": (47.4504, 8.5624),
    "Basel EuroAirport": (47.6008, 7.5320),
    "Genève-Aéroport": (46.2312, 6.1100)
}

ski_resort_municipalities = {
    "Zermatt": (46.0242, 7.7485),
    "St. Moritz": (46.4980, 9.8457),
    "Verbier": (46.0967, 7.2287),
    "Davos": (46.7954, 9.8202),
    "Gstaad": (46.4753, 7.2842),
    "Orsières": (46.0280, 7.1440),
    "Morgins": (46.2374, 6.8529),
    "Anniviers": (46.2054, 7.6025),
    "Grindelwald": (46.6246, 8.0341),
    "Wengen": (46.6050, 7.9209),
    "Mürren": (46.5606, 7.8930),
    "Saas-Fee": (46.1102, 7.9276),
    "Arosa": (46.7839, 9.6793),
    "Lenzerheide": (46.7275, 9.5584),
    "Crans-Montana": (46.3208, 7.4991),
    "Andermatt": (46.6369, 8.5936),
    "Flims": (46.8359, 9.2973),
    "Laax": (46.8204, 9.2660),
    "Falera": (46.8007, 9.2319),
    "Engelberg": (46.8195, 8.4025),
    "Adelboden": (46.4907, 7.5565),
    "Sörenberg": (46.8219, 8.0351),
    "Flumserberg": (47.0925, 9.2808),
    "Braunwald": (46.9423, 8.9984),
    "Saas-Grund": (46.1102, 7.9273),
    "Saas-Almagell": (46.0944, 7.9575),
    "Pontresina": (46.4908, 9.8967),
    "Klosters": (46.8697, 9.8810),
    "Airolo": (46.5277, 8.6091),
    "Zinal": (46.1381, 7.6240),
    "Evolène": (46.1150, 7.4950),
    "Les Crosets": (46.1839, 6.8343),
    "Bergün": (46.6311, 9.7471),
    "Riederalp": (46.3786, 8.0350),
    "Bettmeralp": (46.3713, 8.0773),
    "Fiesch": (46.4062, 8.1344),
    "Sils": (46.4353, 9.7675),
    "Maloja": (46.4017, 9.6950),
    "Frutigen": (46.5888, 7.6513),
    "Lenk": (46.4586, 7.4436),
    "Meiringen": (46.7274, 8.1842),
    "Hasliberg": (46.7452, 8.1950),
    "Alpthal": (47.0841, 8.7265),
    "Oberiberg": (47.0407, 8.7810),
    "Unteriberg": (47.0574, 8.8034),
    "Wildhaus": (47.2031, 9.3512),
    "Unterwasser": (47.1948, 9.3096),
    "Alt St. Johann": (47.1937, 9.2837),
    "Bad Ragaz": (47.0103, 9.5052),
    "Wangs": (47.0319, 9.4329)
}

#Steuersatz pro Kanton
kanton_tax_rates = {
    'ZG': 22.2,
    'AI': 23.8,
    'NW': 24.7,
    'OW': 24.8,
    'SZ': 25.3,
    'UR': 25.3,
    'SH': 29.5,
    'LU': 30.6,
    'AR': 30.7,
    'GL': 31.9,
    'GR': 32.2,
    'SG': 32.4,
    'SO': 33.7,
    'AG': 34.5,
    'FR': 35.3,
    'VS': 36.5,
    'NE': 38.1,
    'JU': 39.0,
    'ZH': 39.8,
    'TI': 40.1,
    'BS': 40.5,
    'BE': 41.2,
    'VD': 41.5,
    'BL': 42.2,
    'GE': 45.0
}

grocery_tags = [("shop", "supermarket"), ("shop", "convenience")]
bank_tags = [("amenity", "bank"), ("amenity", "atm")]
medical_tags = [("amenity", "hospital"), ("amenity", "clinic"), ("amenity", "doctors"), ("amenity", "pharmacy")]
post_tags = [("amenity", "post_office")]


# In[97]:


def clean_address(address):
    address_match = re.search(r'(\d{4})', address)
    if address_match:
        index = address_match.end()  # end position of the postal code
        cleaned = address[:index].strip() + ", Switzerland"
        return cleaned
    return address  # fallback if no postal code found

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1,
        'addressdetails': 1
    }
    headers = {'User-Agent': 'REScrape/1.0 (raoul.tschudin@gmail.com)'}  # required
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        kanton = data[0]['address'].get('state')  # das ist der Kanton
        return lat, lon, kanton
    return None, None, None

def find_nearest_station(lat, lon, limit=20):
    url = "https://transport.opendata.ch/v1/locations"
    params = {
        'x': lon,
        'y': lat,
        'type': 'station',
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['stations']:
        station = data['stations'][1]
        return station['name'], station['distance']
    return None, float("inf")

def find_nearest_train_station(lat, lon, limit=50):
    import requests

    url = "https://transport.opendata.ch/v1/locations"
    params = {
        'x': lon,
        'y': lat,
        'type': 'station',
        'limit': limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    icon_match = None
    name_match = None

    if data.get('stations'):
        for station in data['stations']:
            name = (station.get('name') or '').lower()
            id_ = (station.get('id') or '').lower()
            icon = station.get('icon') or ''

            # Prioritize stations with icon 'train'
            if 'train' in icon and icon_match is None:
                icon_match = (station['name'], station['distance'])

            # Fallback: check for name/id match
            elif any(keyword in name or keyword in id_ for keyword in ['rail', 'bahnhof', 'gare', 'stazione']) and name_match is None:
                name_match = (station['name'], station['distance'])

    if icon_match:
        return icon_match
    elif name_match:
        return name_match
    else:
        return None, None

def get_pm10_from_geotiff(tiff_path, lat, lon):
    # Convert WGS84 (EPSG:4326) to CH1903+ / LV95 (EPSG:2056)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
    x_ch, y_ch = transformer.transform(lon, lat)  # correct order: lon, lat

    # Open the GeoTIFF file
    with rasterio.open(tiff_path) as src:
        # Convert CH1903+ coordinates to row/col in raster
        row, col = src.index(x_ch, y_ch)
        
        # Read the value
        value = src.read(1)[row, col]
        
        # Handle nodata
        if value == src.nodata:
            return None
        return value

def get_strassenlaerm_from_geotiff(tiff_path_1, tiff_path_2, lat, lon):
    # Convert WGS84 (EPSG:4326) to CH1903+ / LV95 (EPSG:2056)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
    x_ch, y_ch = transformer.transform(lon, lat)  # correct order: lon, lat

    # Open the GeoTIFF file
    with rasterio.open(tiff_path_1) as src:
        # Convert CH1903+ coordinates to row/col in raster
        row_1, col_1 = src.index(x_ch, y_ch)
        
        # Read the value
        value_1 = src.read(1)[row_1, col_1]

        # Open the GeoTIFF file
    with rasterio.open(tiff_path_2) as src:
        # Convert CH1903+ coordinates to row/col in raster
        row_2, col_2 = src.index(x_ch, y_ch)
        
        # Read the value
        value_2 = src.read(1)[row_2, col_2]
        
        # Handle nodata
        if value_1 == src.nodata and value_2 == src.nodata:
            return None
    return max(value_1, value_2)

def get_bahnlaerm_from_geotiff(tiff_path_1, tiff_path_2, lat, lon):
    # Convert WGS84 (EPSG:4326) to CH1903+ / LV95 (EPSG:2056)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=True)
    x_ch, y_ch = transformer.transform(lon, lat)  # correct order: lon, lat

    # Open the GeoTIFF file
    with rasterio.open(tiff_path_1) as src:
        # Convert CH1903+ coordinates to row/col in raster
        row_1, col_1 = src.index(x_ch, y_ch)
        
        # Read the value
        value_1 = src.read(1)[row_1, col_1]

        # Open the GeoTIFF file
    with rasterio.open(tiff_path_2) as src:
        # Convert CH1903+ coordinates to row/col in raster
        row_2, col_2 = src.index(x_ch, y_ch)
        
        # Read the value
        value_2 = src.read(1)[row_2, col_2]
        
        # Handle nodata
        if value_1 == src.nodata and value_2 == src.nodata:
            return None
    return max(value_1, value_2)

def closest_swiss_hub(lat, lon):
    property_location = (lat, lon)
    closest_hub = None
    shortest_distance = float("inf")
    for city, city_coords in swiss_hubs.items():
        dist = geopy_distance(property_location, city_coords).meters
        if dist < shortest_distance:
            shortest_distance = dist
            closest_hub = city
    return closest_hub, round(shortest_distance)

def closest_swiss_city(lat, lon):
    property_location = (lat, lon)
    closest_city = None
    shortest_distance = float("inf")
    for city, city_coords in swiss_big_cities.items():
        dist = geopy_distance(property_location, city_coords).meters
        if dist < shortest_distance:
            shortest_distance = dist
            closest_city = city
    return closest_city, round(shortest_distance)

def closest_swiss_major_city(lat, lon):
    property_location = (lat, lon)
    closest_major_city = None
    shortest_distance = float("inf")
    for city, city_coords in swiss_major_cities.items():
        dist = geopy_distance(property_location, city_coords).meters
        if dist < shortest_distance:
            shortest_distance = dist
            closest_major_city = city
    return closest_major_city, round(shortest_distance)

def closest_swiss_major_airport(lat, lon):
    property_location = (lat, lon)
    closest_major_airport = None
    shortest_distance = float("inf")
    for airport, airport_coords in swiss_major_airports.items():
        dist = geopy_distance(property_location, airport_coords).meters
        if dist < shortest_distance:
            shortest_distance = dist
            closest_major_airport = airport
    return closest_major_airport, round(shortest_distance)

def closest_holiday_area(lat, lon):
    property_location = (lat, lon)
    closest_holiday_area = None
    shortest_distance = float("inf")
    for holiday_municipality, holiday_municipality_coords in ski_resort_municipalities.items():
        dist = geopy_distance(property_location, holiday_municipality_coords).meters
        if dist < shortest_distance:
            shortest_distance = dist
            closest_holiday_area = holiday_municipality
    return closest_holiday_area, round(shortest_distance)

def get_commute_time(from_place, to_place, limit=1):
    url = "https://transport.opendata.ch/v1/connections"
    params = {
        'from': from_place,
        'to': to_place,
        'limit': limit
    }
    response = requests.get(url, params=params)
    data = response.json()

    if 'connections' in data and data['connections']:
        # Example format: "00d01:05:00" or "01:05:00"
        duration_str = data['connections'][0]['duration']
        duration_str = duration_str.replace('d', '')  # Remove 'd' if present
        time_parts = duration_str.split(':')
        if len(time_parts) == 3:
            h, m, s = map(int, time_parts)
        elif len(time_parts) == 2:
            h, m = map(int, time_parts)
        else:
            return None  # Unexpected format
        total_minutes = h * 60 + m
        return total_minutes
    return None

def find_nearby_schools(lat, lon, radius=5000):
    query = f"""
    [out:json];
    (
      node["amenity"~"school|kindergarten|university|college"](around:{radius},{lat},{lon});
      way["amenity"~"school|kindergarten|university|college"](around:{radius},{lat},{lon});
      relation["amenity"~"school|kindergarten|university|college"](around:{radius},{lat},{lon});
    );
    out center;
    """
    
    response = requests.post("https://overpass-api.de/api/interpreter", data={"data": query})
    data = response.json()

    results = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unnamed School")
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")
        if lat and lon:
            results.append((name, lat, lon))
    return results

def distance_to_nearest_school(lat, lon, schools):
    user_location = (lat, lon)
    if not schools:
        return None  # No schools found
    distances = [geodesic(user_location, (s_lat, s_lon)).meters for _, s_lat, s_lon in schools]
    return min(distances)

def find_osm_amenities(lat, lon, radius, tags):
    """
    tags: List of tuples like [("shop", "supermarket"), ("amenity", "bank")]
    """
    query_parts = []
    for key, value in tags:
        query_parts.append(f'node["{key}"="{value}"](around:{radius},{lat},{lon});')
        query_parts.append(f'way["{key}"="{value}"](around:{radius},{lat},{lon});')
        query_parts.append(f'relation["{key}"="{value}"](around:{radius},{lat},{lon});')
    
    query = f"""
    [out:json];
    (
      {"".join(query_parts)}
    );
    out center;
    """
    
    response = requests.post("https://overpass-api.de/api/interpreter", data={"data": query})
    data = response.json()

    results = []
    for element in data.get("elements", []):
        name = element.get("tags", {}).get("name", "Unnamed")
        e_lat = element.get("lat") or element.get("center", {}).get("lat")
        e_lon = element.get("lon") or element.get("center", {}).get("lon")
        if e_lat and e_lon:
            results.append((name, e_lat, e_lon))
    return results

def find_osm_nature_features(lat, lon, radius=1000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][timeout:25];
    (
        node["leisure"](around:{radius},{lat},{lon});
        node["landuse"](around:{radius},{lat},{lon});
        node["natural"](around:{radius},{lat},{lon});
        way["leisure"](around:{radius},{lat},{lon});
        way["landuse"](around:{radius},{lat},{lon});
        way["natural"](around:{radius},{lat},{lon});
        node["highway"="path"](around:{radius},{lat},{lon});
        way["highway"="path"](around:{radius},{lat},{lon});
        relation["route"~"hiking|bicycle"](around:{radius},{lat},{lon});
    );
    out center;
    """

    response = requests.get(overpass_url, params={'data': query})
    data = response.json()

    nature_pois = []
    for element in data['elements']:
        name = element.get('tags', {}).get('name', 'Unnamed Nature Spot')
        lat_ = element.get('lat')
        lon_ = element.get('lon')
        if lat_ and lon_:
            nature_pois.append((name, lat_, lon_))
    return nature_pois

def distance_to_nearest(lat, lon, poi_list):
    if not poi_list:
        return None
    user_location = (lat, lon)
    distances = [geodesic(user_location, (p_lat, p_lon)).meters for _, p_lat, p_lon in poi_list]
    return min(distances)

def get_tax_score(kanton):
    tax = kanton_tax_rates.get(kanton)
    if tax is None:
        return 0.5  # Neutraler Wert, wenn unbekannt

    # Skalierung: je niedriger der Steuerfuss, desto näher an 1.0
    # 22% → 1.0 ; 45% → 0.0
    min_tax, max_tax = 22.2, 45.01
    tax_score = 1 - (tax - min_tax) / (max_tax - min_tax)
    return round(tax_score, 3)

def get_regional_importance_score(city_name):
    return regional_importance.get(city_name, regional_importance['DEFAULT'])

def calculate_location_score(lat, lon):
    # Get distances
    nearest_station = find_nearest_station(lat, lon)[0] or ""
    hub = closest_swiss_hub(lat, lon)[0] or ""
    hub_commute_time = get_commute_time(nearest_station, hub, limit=1)
    if hub_commute_time is None:
        hub_commute_time = 999
    city = closest_swiss_city(lat, lon)[0] or ""
    city_commute_time = get_commute_time(nearest_station, city, limit=1)
    if city_commute_time is None:
        city_commute_time = 999
    major_city = closest_swiss_major_city(lat, lon)[0] or ""
    major_city_commute_time = get_commute_time(nearest_station, major_city, limit=1)
    if major_city_commute_time is None:
        major_city_commute_time = 999
    major_airport = closest_swiss_major_airport(lat, lon)[0] or ""
    major_airport_commute_time = get_commute_time(nearest_station, major_airport, limit=1)
    if major_airport_commute_time is None:
        major_airport_commute_time = 999
    _, station_dist = find_nearest_station(lat, lon)
    if station_dist is None:
        station_dist = 999
    _, train_station_dist = find_nearest_train_station(lat, lon)
    if train_station_dist is None:
        train_station_dist = 1500
    school_dist = distance_to_nearest_school(lat, lon, find_nearby_schools(lat, lon))
    if school_dist is None:
        school_dist = 3000
    grocery_dist = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 3000, grocery_tags))
    if grocery_dist is None:
        grocery_dist = 5000
    bank_dist = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 3000, bank_tags))
    if bank_dist is None:
        bank_dist = 5000
    medical_dist = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 5000, medical_tags))
    if medical_dist is None:
        medical_dist = 7000
    post_dist = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 5000, post_tags))
    if post_dist is None:
        post_dist = 5000
    nature_pois = find_osm_nature_features(lat, lon, radius=1000)
    nature_occurrences = len(nature_pois)
    nature_dist = distance_to_nearest(lat, lon, nature_pois)
    if nature_dist is None:
        nature_dist = 3000
    air_quality = get_pm10_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/luftreinhaltung-feinstaub_pm10_2023_2056.tif", lat, lon)
    if air_quality is None:
        air_quality = 35
    street_noise = get_strassenlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Nacht_LV95.tif", lat, lon) or 0
    rail_noise = get_bahnlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Nacht_LV95.tif", lat, lon) or 0
    noise_exposure = max(street_noise, rail_noise)
    if noise_exposure is None:
        noise_exposure = 45
    
    # Normalize each distance (max reasonable distances in meters)
    hub_score = 1 - min(hub_commute_time, 20) / 20
    city_score = 1 - min(city_commute_time, 30) / 30
    major_city_score = 1 - min(major_city_commute_time, 60) / 60
    major_airport_score = 1 - min(major_airport_commute_time, 150) / 150
    school_score = 1 - min(school_dist, 3000) / 3000
    station_score = 1 - min(station_dist, 2500) / 2500
    train_station_score = 1 - min(train_station_dist, 5000) / 5000
    grocery_score = 1 - min(grocery_dist, 1500) / 1500
    bank_score = 1 - min(bank_dist, 1500) / 1500
    medical_score = 1 - min(medical_dist, 3000) / 3000
    post_score = 1 - min(post_dist, 2000) / 2000
    nature_distance_score = 1 - min(nature_dist, 1000) / 1000
    nature_density_score = min(nature_occurrences, 25) / 25
    nature_score = 0.2 * nature_distance_score + 0.8 * nature_density_score
    air_score = 1 - min(air_quality, 60) / 60
    noise_score = 1 - min(noise_exposure, 80) / 80
    
    # Calculate amenity_score for overall location_score (you can tweak these weights!)
    amenity_score = (
    0.4 * grocery_score +
    0.25 * bank_score +
    0.2 * medical_score +
    0.15 * post_score
)

    regional_importance_score = get_regional_importance_score(major_city)
    tax_score = get_tax_score(geocode_address(cleaned_address)[2])
    # Weighted average (you can tweak these weights!)
    overall_score = (
        0.02 * hub_score +
        0.02 * city_score +
        0.15 * major_city_score +
        0.10 * major_airport_score +
        0.05 * school_score +
        0.05 * amenity_score +
        0.06 * nature_score +
        0.05 * noise_score +
        0.05 * air_score + 
        0.10 * station_score +
        0.20 * train_station_score +
        0.12 * regional_importance_score +
        0.03 * tax_score
    )

    return round(overall_score, 3)


# In[94]:


cleaned_address = clean_address("Chemin de la Larisse 19, 1653 Châtel-sur-Montsalvens")
print(cleaned_address)
coordinates = geocode_address(cleaned_address)[0], geocode_address(cleaned_address)[1]
print(coordinates)
lat = coordinates[0]
lon = coordinates [1]
print(find_osm_nature_features(lat, lon, radius=1000))
print(get_pm10_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/luftreinhaltung-feinstaub_pm10_2023_2056.tif", lat, lon))
print(get_strassenlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Nacht_LV95.tif", lat, lon))
print(get_bahnlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Nacht_LV95.tif", lat, lon))
print(closest_swiss_hub(lat, lon))
print(closest_swiss_city(lat, lon))
print(closest_swiss_major_city(lat, lon))
print(find_nearest_station(lat, lon))
print(find_nearest_train_station(lat, lon))
print(calculate_location_score(lat, lon))
print(closest_swiss_major_airport(lat, lon))
print(distance_to_nearest_school(lat, lon, find_nearby_schools(lat, lon)))
print(get_commute_time(find_nearest_station(lat, lon)[0], closest_swiss_major_city(lat, lon)[0], limit=1))
print(get_commute_time(find_nearest_station(lat, lon)[0], closest_swiss_city(lat, lon)[0], limit=1))
print(get_commute_time(find_nearest_station(lat, lon)[0], closest_swiss_major_airport(lat, lon)[0], limit=1))


# In[99]:


#-------START SCRAPING-------

#initialize chrome driver with options to stop webpages from freezing/infinite loading
# Start the WebDriver with logging enabled (use `uc=False` for simpler testing)
ua = UserAgent()
db = ZipcodesDatabase('/tmp/zipcodes')
def create_browser():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")  # Disable sandbox (use with caution)
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--disable-plugins")  # Disable plugins
    chrome_options.add_argument("--disable-background-networking")  # Disable background networking
    chrome_options.add_argument("--disable-background-tasks")  # Disable background tasks
    chrome_options.add_argument("--disable-hardware-acceleration")  # Disable hardware acceleration (use if necessary)
    chrome_options.add_argument("--disable-features=IsolateOrigins,site-per-process")  # Avoid origin issues
    chrome_options.add_argument("--disable-remote-fonts")  # Disable remote fonts
    chrome_options.add_argument("--disable-client-side-phishing-detection")  # Avoid delays from phishing detection
    chrome_options.add_argument("--disable-software-rasterizer")  # Avoid software rendering if unnecessary
    chrome_options.add_argument("--disable-timed-header")  # Prevent timing issues in loading
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument(f"user-agent={ua.random}")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

#maybe remove headless mode to enable easier page loading
    #chrome_options.add_argument("--headless")  # Optional, but avoid if possible
    driver = Driver(uc=True)  # seleniumbase will manage Chrome options automatically
    driver.set_page_load_timeout(600)
    driver.driver = webdriver.Chrome(options=chrome_options)  # Override driver with our custom options
    driver.delete_all_cookies()
    return driver

#Handle page freeze and infinite loading
def restart_browser(link):
    print("initialising browser refresh")
    max_retries = 1  # Limit retries to avoid infinite loops
    retry_count = 0
    global driver
    while retry_count < max_retries:
        try:
            print("attempt " + str(retry_count) + " of trying to refresh the browser")
            driver.refresh()
            WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "ResultListPage_searchBarWrapper_lqBY2")),
                    EC.presence_of_element_located((By.CLASS_NAME, "spotlight-components")))
    )
            print("Results page loaded successfully.")
            break  # Exit the loop if successful
        except (TimeoutException, ReadTimeoutError) as e:
            print("browser refresh attempt " + str(retry_count) + " failed")
            print(f"Error encountered: {e}")
            retry_count += 1
            # Quit driver before reinitialising
            # Re-create browser after quitting previous instance
    if retry_count == max_retries:
        print("Max retries reached. Exiting script.")
        print("killing browser")
        subprocess.call("pkill -f chrome", shell=True)
        print("quitting browser")
        driver.quit()
        time.sleep(5) # Wait before reopening browser
        driver = create_browser()
        driver.get(link)
        try:
            cookie_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
            cookie_element.click()
        except Exception as e:
            print("No cookie-request")

def random_mouse_movement(duration=10):
    screen_width, screen_height = pyautogui.size()
    start_time = time.time()
    
    while time.time() - start_time < duration:
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        duration = random.uniform(0.1, 0.5)  # move time
        pyautogui.moveTo(x, y, duration)
        time.sleep(random.uniform(0.2, 1.0))  # pause between moves

def random_scroll():
    for _ in range(random.randint(5, 15)):
        scroll_amount = random.randint(-10, 10)
        pyautogui.scroll(scroll_amount)
        time.sleep(random.uniform(0.2, 1.0))

driver = create_browser()
# Go to the page
driver.get("https://www.homegate.ch/de")

# Step 1: Accept cookies
try:
    cookie_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'onetrust-accept-btn-handler')))
finally:
    cookie_element.click()

random_mouse_movement(10)
random_scroll()

# Step 2: Click "Kaufen" button
Kaufen_button = driver.find_element(By.XPATH, "//*[@id='app']/main/div/div[1]/div[2]/div/ul/li[2]")
Kaufen_button.click()

# Step 3: Enter location (e.g., "Schweiz")
location_button = driver.find_element(By.XPATH, "//*[@id='app']/main/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div[1]/span")
location_button.click()

random_mouse_movement(8)
random_scroll()

try:
    search_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='app']/main/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/input"))
    )
    search_field.send_keys("Schweiz")
    search_field.send_keys(Keys.RETURN)
except Exception as e:
    print("Search field not found:", e)

try:
    select_country_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='app']/main/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div/div[2]/div[2]/p[1]"))
    )
finally:
    time.sleep(random.randint(1, 7))
    select_country_button.click()

# Step 4: Enter "Treffer" button (updated)
time.sleep(5)

random_mouse_movement(10)
random_scroll()

try:
    #Wait until Treffer button updates itself and is ready
    treffer_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='app']/main/div/div[1]/div[2]/div/div/div[2]/div/div/div[5]")))
    # Wait a bit more and check visibility. Helps avoiding Cloudflare detection
    time.sleep(random.randint(1, 7))
    click_or_enter = random.randint(1, 2)
    if click_or_enter == 1:
        ActionChains(driver).move_to_element(treffer_button).pause(random.uniform(0.5, 1.2)).click().perform()
    else:
    #Press 5 times tab and then enter to hit the search for listings/results
        N=5
        actions = ActionChains(driver) 
        for _ in range(N):
            actions = actions.send_keys(Keys.TAB)
        actions.perform()
        actions.send_keys(Keys.ENTER).perform()

    # Scroll the page down to load more content incrementally. Added this to avoid Cloudflare detection. Not sure if really necessary
    for _ in range(10):  # Adjust the number of scrolls based on your requirements
        driver.execute_script("window.scrollTo(0, 1080)")
        time.sleep(2)  # Give time for content to load
    # Wait for an element on the results page to confirm transition
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ResultListPage_searchBarWrapper_lqBY2"))  # Update this to a unique class or ID on the results page
    )
    print("Results page loaded successfully. 1st time")
except Exception as e:
#If page does not load properly first time. Exception repeats page refresh until it works.
    print(f"Error: {e}")
    restart_browser("https://www.homegate.ch/kaufen/immobilien/land-schweiz/trefferliste")

def get_re_data(page_number):
    print("initialising data extraction")
    page_number += 1
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ResultListPage_searchBarWrapper_lqBY2"))  # Update this to a unique class or ID on the results page
    )
    global nutzflaeche
    global raumhoehe
    global baujahr
    global zimmeranzahl
    global etage
    global kanton
    global wohnflaeche
    global objekttyp
    global haustiere_erlaubt
    global balkon_terrasse
    global geschirrspueler
    global cheminee
    global kabel_tv
    global aussicht
    global aussicht_berge
    global rollstuhlgaengig
    global ruhige_lage
    global kinderfreundlich
    global parkplatz
    global garage
    global lift
    global neubau
    global minergie_zertifiziert
    global minergie_bauweise
    global hochparterre
    current_listings_webpage = driver.current_url
    print(type(current_listings_webpage), current_listings_webpage) 
    time.sleep(random.randint(2, 9))
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".ResultList_listItem_j5Td_ a")))
    listings_page = driver.find_elements(By.CSS_SELECTOR, ".ResultList_listItem_j5Td_ a")
    time.sleep(random.randint(2, 9))
    print(driver.page_source[:2000])  # Print beginning of page
    print(listings_page)
    hrefs = []
    for listing in listings_page:
        print(listing)
        hrefs.append(listing.get_attribute("href"))
    print(hrefs)
    for real_estate_object in hrefs:
        print(real_estate_object)
        
        #-------------------
        #Reset all variables
        #-------------------
        
        #General variables
        name_re_object = ""
        currency_cleaned = ""
        price_cleaned = ""
        coordinates = (None, None)
        changed_address = 0
        
        #Transport
        nearest_station = ""
        distance_nearest_station = float("inf")
        nearest_train_station = ""
        distance_nearest_train_station = float("inf")
        
        #Cities & Commutes
        closest_hub = ""
        distance_closest_swiss_hub = float("inf")
        commute_time_hub = float("inf")
        closest_city = ""
        distance_closest_swiss_city = float("inf")
        commute_time_city = float("inf")
        closest_major_city = ""
        distance_closest_major_city = float("inf")
        commute_time_major_city = float("inf")
        closest_major_airport = ""
        distance_closest_major_airport = float("inf")
        commute_time_major_airport = float("inf")
        holiday_region = 0
        closest_holiday_region = ""
        distance_closest_holiday_region = float("inf")
        commute_time_closest_holiday_region = float("inf")
        
        #Amenities
        distance_nearest_school = float("inf")
        distance_nearest_grocery = float("inf")
        distance_nearest_bank = float("inf")
        distance_nearest_medical = float("inf")
        distance_nearest_post = float("inf")
        
        #Nature
        distance_nearest_nature = float("inf")
        nature_occurrences = 0
        nature_density = 0.0
        nature_pois = []
        
        #Environment
        pm10_value = None
        street_noise_exposure = None
        rail_noise_exposure = None
        max_noise_exposure = None
        
        #Location
        postal_code = ""
        region = ""
        kanton = ""
        tax_rate_canton = None
        location_score = 0.0
        address = ""
        
        #Features
        nutzflaeche = ""
        raumhoehe = ""
        baujahr = ""
        number_of_rooms = ""
        living_space = ""
        zimmeranzahl = ""
        etage = ""
        wohnflaeche = ""
        objekttyp = ""
        
        #Booleans
        haustiere_erlaubt = 0
        balkon_terrasse = 0
        geschirrspueler = 0
        cheminee = 0
        kabel_tv = 0
        aussicht = 0
        aussicht_berge = 0
        rollstuhlgaengig = 0
        ruhige_lage = 0
        kinderfreundlich = 0
        parkplatz = 0
        garage = 0
        lift = 0
        neubau = 0
        minergie_zertifiziert = 0
        minergie_bauweise = 0
        hochparterre = 0
        
        #-------------------
        #Reset end
        #-------------------
        
        try:
            driver.get(real_estate_object)
            real_estate_object_id = real_estate_object.rstrip("/").split("/")[-1]
            time.sleep(random.randint(2, 9))
            name_re_object = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spotlight-components h1"))).get_attribute("innerHTML")
            print("Type of input:", type(name_re_object), "Value:", name_re_object)
            #price_element = driver.find_element(By.CLASS_NAME, "SpotlightAttributesPrice_value_TqKGz")
            price_element = driver.find_element(By.CSS_SELECTOR, "[class^='SpotlightAttributesPrice_value_']")
            print("Type of input:", type(price_element), "Value:", price_element)
            price_text = price_element.text
            print("Type of input:", type(price_text), "Value:", price_text)
            currency_cleaned = price_text.split()[0]
            print("Type of input:", type(currency_cleaned), "Value:", currency_cleaned)
            price_cleaned = price_text.replace('CHF', '').replace('’', '').replace('.–', '').strip()  # Remove 'CHF' and any extra spaces
            print("Type of input:", type(price_cleaned), "Value:", price_cleaned)
            #rooms_element = driver.find_element(By.CLASS_NAME, "SpotlightAttributesNumberOfRooms_value_TUMrd")
            rooms_element = driver.find_element(By.CSS_SELECTOR, "[class^='SpotlightAttributesNumberOfRooms_value_']")
            print("Type of input:", type(rooms_element), "Value:", rooms_element)
            number_of_rooms = rooms_element.text
            print("Type of input:", type(number_of_rooms), "Value:", number_of_rooms)
            try:
                #living_space_element = driver.find_element(By.CLASS_NAME, "SpotlightAttributesUsableSpace_value_cpfrh")
                living_space_element = driver.find_element(By.CSS_SELECTOR, "[class^='SpotlightAttributesUsableSpace_value_']")
                print("Type of input:", type(living_space_element), "Value:", living_space_element)
                living_space = living_space_element.text
                print("Type of input:", type(living_space), "Value:", living_space)
            except NoSuchElementException:
                living_space = ""
            #address_element = driver.find_element(By.CLASS_NAME, "AddressDetails_address_i3koO")
            address_element = driver.find_element(By.CSS_SELECTOR, "[class^='AddressDetails_address_']")
            print("Type of input:", type(address_element), "Value:", address_element)
            address = address_element.text
            print("Type of input:", type(address), "Value:", address)
            #LOCATION_VARIABLES_START-------------------------------
            #_____!!!!!_____!!!!!_____!!!!!_____!!!!!_____!!!!!_____!!!!!
            cleaned_address = clean_address(address)
            coordinates = geocode_address(cleaned_address)[0], geocode_address(cleaned_address)[1]
            lat = coordinates[0]
            lon = coordinates [1]
            if lat is None or lon is None:
                print("Address could not be found. Simplifying address.")
                simplified_address = re.sub(r"(?i)(chemin|route|rue|allee|avenue|impasse|quai|platz|weg|via|cours|allee)\s+de\s+", "", cleaned_address)
                coordinates = geocode_address(simplified_address)[0], geocode_address(simplified_address)[1]
                lat = coordinates[0]
                lon = coordinates [1]
                if lat is None or lon is None:
                    print("Address simplification not successful. Using fallback value.")
                    changed_address = 1
                    match = re.search(r'(\d{4})\s+(.+)', address)
                    if match:
                        print("Using postal code and municipality as fallback address")
                        fallback_address = f"{match.group(1)} {match.group(2)}, Switzerland"
                    else:
                        print("Using Switzerland as fallback address")
                        fallback_address = "Switzerland"
                    fallback_coordinates = geocode_address(fallback_address)[0], geocode_address(fallback_address)[1]
                    lat = fallback_coordinates[0]
                    lon = fallback_coordinates[1]
            pm10_value = get_pm10_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/luftreinhaltung-feinstaub_pm10_2023_2056.tif", lat, lon)
            print("Type of input:", type(pm10_value), "Value:", pm10_value)
            street_noise_exposure = get_strassenlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/StrassenLaerm_Nacht_LV95.tif", lat, lon) or 0
            print("Type of input:", type(street_noise_exposure), "Value:", street_noise_exposure)
            rail_noise_exposure = get_bahnlaerm_from_geotiff("/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Tag_LV95.tif", "/Users/raoultschudin/Desktop/RE_scrape/Bahnlaerm_Nacht_LV95.tif", lat, lon) or 0
            print("Type of input:", type(rail_noise_exposure), "Value:", rail_noise_exposure)
            max_noise_exposure = max(street_noise_exposure, rail_noise_exposure)
            print("Type of input:", type(max_noise_exposure), "Value:", max_noise_exposure)
            closest_hub = closest_swiss_hub(lat, lon)[0]
            print("Type of input:", type(closest_hub), "Value:", closest_hub)
            distance_closest_swiss_hub = closest_swiss_hub(lat, lon)[1]
            print("Type of input:", type(distance_closest_swiss_hub), "Value:", distance_closest_swiss_hub)
            closest_city = closest_swiss_city(lat, lon)[0]
            print("Type of input:", type(closest_city), "Value:", closest_city)
            distance_closest_swiss_city = closest_swiss_city(lat, lon)[1]
            print("Type of input:", type(distance_closest_swiss_city), "Value:", distance_closest_swiss_city)
            closest_major_city = closest_swiss_major_city(lat, lon)[0]
            print("Type of input:", type(closest_major_city), "Value:", closest_major_city)
            distance_closest_major_city = closest_swiss_major_city(lat, lon)[1]
            print("Type of input:", type(distance_closest_major_city), "Value:", distance_closest_major_city)
            closest_major_airport = closest_swiss_major_airport(lat, lon)[0]
            print("Type of input:", type(closest_major_airport), "Value:", closest_major_airport)
            distance_closest_major_airport = closest_swiss_major_airport(lat, lon)[1]
            print("Type of input:", type(distance_closest_major_airport), "Value:", distance_closest_major_airport)
            nearest_station = find_nearest_station(lat, lon)[0]
            print("Type of input:", type(nearest_station), "Value:", nearest_station)
            distance_nearest_station = find_nearest_station(lat, lon)[1]
            print("Type of input:", type(distance_nearest_station), "Value:", distance_nearest_station)
            nearest_train_station = find_nearest_train_station(lat, lon)[0]
            print("Type of input:", type(nearest_train_station), "Value:", nearest_train_station)
            distance_nearest_train_station = find_nearest_train_station(lat, lon)[1] or 9999
            print("Type of input:", type(distance_nearest_train_station), "Value:", distance_nearest_train_station)
            commute_time_hub = get_commute_time(nearest_station, closest_hub, limit=1) or 999
            print("Type of input:", type(commute_time_hub), "Value:", commute_time_hub)
            commute_time_major_city = get_commute_time(nearest_station, closest_major_city, limit=1) or 999
            print("Type of input:", type(commute_time_major_city), "Value:", commute_time_major_city)
            commute_time_city = get_commute_time(nearest_station, closest_city, limit=1) or 999
            print("Type of input:", type(commute_time_city), "Value:", commute_time_city)
            commute_time_major_airport = get_commute_time(nearest_station, closest_major_airport, limit=1) or 999
            print("Type of input:", type(commute_time_major_airport), "Value:", commute_time_major_airport)
            distance_nearest_school = distance_to_nearest_school(lat, lon, find_nearby_schools(lat, lon))
            print("Type of input:", type(distance_nearest_school), "Value:", distance_nearest_school)
            distance_nearest_grocery = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 3000, grocery_tags))
            print("Type of input:", type(distance_nearest_grocery), "Value:", distance_nearest_grocery)
            if distance_nearest_grocery is None:
                distance_nearest_grocery = 5000
            distance_nearest_bank = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 3000, bank_tags))
            if distance_nearest_bank is None:
                distance_nearest_bank = 5000
            distance_nearest_medical = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 5000, medical_tags))
            if distance_nearest_medical is None:
                distance_nearest_medical = 7000
            distance_nearest_post = distance_to_nearest(lat, lon, find_osm_amenities(lat, lon, 5000, post_tags))
            if distance_nearest_post is None:
                distance_nearest_post = 5000
            nature_pois = find_osm_nature_features(lat, lon, radius=1000)
            nature_occurrences = len(nature_pois)
            nature_density = min(nature_occurrences, 25) / 25
            distance_nearest_nature = distance_to_nearest(lat, lon, nature_pois)
            if distance_nearest_nature is None:
                distance_nearest_nature = 3000
            #LOCATION_VARIABLES_END--------------------------------------
            #_____!!!!!_____!!!!!_____!!!!!_____!!!!!_____!!!!!_____!!!!!
            dt_elements = driver.find_elements(By.TAG_NAME, "dt")
            heading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//h2[contains(text(), 'Merkmale und Ausstattung')]")))
            print("Heading found", heading.text)
            print(address)
            match = re.search(r'(\d{4})\s+(.+)$', address)
            print(match)
            if match:
                postal_code = match.group(1)
                print(postal_code)
                region = match.group(2).strip()
                print(region)
                kanton = db.get_location(int(postal_code)).canton
                print(kanton)
                print(type(kanton))
            else:
                postal_code = "0000"
                region = "None"
                kanton = "None"
            closest_holiday_region = closest_holiday_area(lat, lon)[0]
            distance_closest_holiday_region = closest_holiday_area(lat, lon)[1]
            if region in ski_resort_municipalities.keys():
                holiday_region = 1
            if distance_closest_holiday_region <= 7500:
                holiday_region = 1
            commute_time_holiday_region = get_commute_time(nearest_station, closest_holiday_region, limit=1) or 999
            tax_rate_canton = kanton_tax_rates.get(kanton)
            print(tax_rate_canton)
            location_score = calculate_location_score(lat, lon)
            print(location_score)
            try:
                merkmale_elements = driver.find_elements(By.CSS_SELECTOR, "[class^='FeaturesFurnishings_list_']")
                if merkmale_elements:
                    merkmale_items = merkmale_elements[0].find_elements(By.TAG_NAME, "li")
                    for item in merkmale_items:
                        merkmal_text = item.text.strip()
                        print(merkmal_text)
                        if "Haustiere erlaubt" in merkmal_text:
                            haustiere_erlaubt = 1
                        elif "Balkon / Terrasse" in merkmal_text:
                            balkon_terrasse = 1
                        elif "Geschirrspüler" in merkmal_text:
                            geschirrspueler = 1
                        elif "Cheminée" in merkmal_text:
                            cheminee = 1
                        elif "Kabel-TV" in merkmal_text:
                            kabel_tv = 1
                        elif "Aussicht" in merkmal_text:
                            aussicht = 1
                        elif "Aussicht auf die Berge" in merkmal_text:
                            aussicht_berge = 1
                        elif "Rollstuhlgängig" in merkmal_text:
                            rollstuhlgaengig = 1
                        elif "Ruhige Lage" in merkmal_text:
                            ruhige_lage = 1
                        elif "Kinderfreundlich" in merkmal_text:
                            kinderfreundlich = 1
                        elif "Parkplatz" in merkmal_text:
                            parkplatz = 1
                        elif "Garage" in merkmal_text:
                            garage = 1
                        elif "Lift" in merkmal_text:
                            lift = 1
                        elif "Neubau" in merkmal_text:
                            neubau = 1
                        elif "Minergie zertifiziert" in merkmal_text:
                            minergie_zertifiziert = 1
                        elif "Minergie Bauweise" in merkmal_text:
                            minergie_bauweise = 1
                        elif "Hochparterre" in merkmal_text:
                            hochparterre = 1
            except Exception as e:
                print("Keine Merkmale & Ausstattung", e)
            for dt in dt_elements:
                dt_text = dt.text.strip()
                if dt_text == "Nutzfläche:":
                    # Get the corresponding <dd> sibling element
                    dd_element_1 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    nutzflaeche = dd_element_1.text.strip()
                    if nutzflaeche is None:
                        nutzflaeche = "missing-value"
                if dt_text == "Raumhöhe:":
                    # Get the corresponding <dd> sibling element
                    dd_element_2 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    raumhoehe = dd_element_2.text.strip()
                    if raumhoehe is None:
                        raumhoehe = "missing-value"
                if dt_text == "Baujahr:":
                    # Get the corresponding <dd> sibling element
                    dd_element_3 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    baujahr = dd_element_3.text.strip()
                    if baujahr is None:
                        baujahr = "missing-value"
                if dt_text == "Anzahl Zimmer:":
                    # Get the corresponding <dd> sibling element
                    dd_element_4 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    zimmeranzahl = dd_element_4.text.strip()
                    if zimmeranzahl is None:
                        zimmeranzahl = "missing-value"
                if dt_text == "Etage:":
                    # Get the corresponding <dd> sibling element
                    dd_element_5 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    etage = dd_element_5.text.strip()
                    if etage is None:
                        etage = "missing-value"
                if dt_text == "Wohnfläche:":
                    # Get the corresponding <dd> sibling element
                    dd_element_6 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    wohnflaeche = dd_element_6.text.strip()
                    if wohnflaeche is None:
                        wohnflaeche = "missing-value"
                if dt_text == "Objekttyp:":
                    # Get the corresponding <dd> sibling element
                    dd_element_7 = dt.find_element(By.XPATH, "following-sibling::dd[1]")
                    objekttyp = dd_element_7.text.strip()
                    if objekttyp is None:
                        objekttyp = "missing-value"
        except Exception as e:
        #If page does not load properly first time. Exception repeats page refresh until it works.
            print(f"Error: {e}")
            restart_browser(real_estate_object)

        print(name_re_object + ' ' + currency_cleaned + ' ' + price_cleaned + ' ' + number_of_rooms + ' ' + living_space + ' ' + address + ' ' + nutzflaeche + ' ' + raumhoehe + ' ' + baujahr + ' ' + zimmeranzahl + ' ' + etage + ' ' + wohnflaeche + ' ' + objekttyp + ' ' + str(haustiere_erlaubt) + ' ' + str(balkon_terrasse) + ' ' + str(geschirrspueler) + ' ' + str(cheminee) + ' ' + str(kabel_tv) + ' ' + str(aussicht) + ' ' + str(aussicht_berge) + ' ' + str(rollstuhlgaengig) + ' ' + str(ruhige_lage) + ' ' + str(kinderfreundlich) + ' ' + str(parkplatz) + ' ' + str(garage) + ' ' + str(lift) + ' ' + str(neubau) + ' ' + str(minergie_zertifiziert) + ' ' + str(minergie_bauweise) + ' ' + str(hochparterre) + ' ' + postal_code + ' ' + region + ' ' + kanton)
        real_estate_data.append({
    "Name": name_re_object,
    "ID": real_estate_object_id,
    "Währung": currency_cleaned,
    "Preis": price_cleaned,
    "Räume": number_of_rooms,
    "Living space": living_space,
    "Adresse": address,
    "Adresse abgeändert": changed_address,
    "Postleitzahl": postal_code,
    "Ortschaft": region,
    "Kanton": kanton,
    "Koordinaten": coordinates,
    "Luftverschmutzung (PM10) - µg/m³": pm10_value,
    "Strassenlärm in dB(A)": street_noise_exposure,
    "Bahnlärm in dB(A)": rail_noise_exposure,
    "Maximaler Lärmpegel in dB(A)": max_noise_exposure,
    "Nächste ÖV Station": nearest_station,
    "Entfernung zu nächster ÖV Station": distance_nearest_station,
    "Nächster Bahnhof": nearest_train_station,
    "Entfernung zu nächstem Bahnhof": distance_nearest_train_station,
    "Entfernung zu nächster Schule": distance_nearest_school,
    "Entfernung zu nächstem Supermarkt": distance_nearest_grocery,
    "Entfernung zu nächster Bank": distance_nearest_bank,
    "Entfernung zu nächster pharmazeutischer Versorgung": distance_nearest_medical,
    "Entfernung zu nächster Post": distance_nearest_post,
    "Entfernung zu Natur": distance_nearest_nature,
    "Naturvorkommnisse im 1km Radius": nature_occurrences,
    "Naturdichte im 1km Radius": nature_density,
    "Nächster Knotenpunkt": closest_hub,
    "Entfernung zu Knotenpunkt": distance_closest_swiss_hub,
    "Pendelzeit zu Knotenpunkt": commute_time_hub,
    "Nächste Stadt": closest_city,
    "Entfernung zu Stadt": distance_closest_swiss_city,
    "Pendelzeit zu Stadt": commute_time_city,
    "Nächste Grossstadt": closest_major_city,
    "Entfernung zu Grossstadt": distance_closest_major_city,
    "Pendelzeit zu Grossstadt": commute_time_major_city,
    "Nächster Flughafen": closest_major_airport,
    "Entfernung zu Flughafen": distance_closest_major_airport,
    "Pendelzeit zu Flughafen": commute_time_major_airport,
    "Feriengebiet": holiday_region,
    "Entfernung Feriengebiet": distance_closest_holiday_region,
    "Pendelzeit zu Feriengebiet": commute_time_closest_holiday_region,
    "Steuerrate des Kantons": tax_rate_canton,
    "Standortbewertung": location_score,
    "Nutzfläche": nutzflaeche,
    "Raumhöhe": raumhoehe,
    "Baujahr": baujahr,
    "Zimmeranzahl": zimmeranzahl,
    "Etage": etage,
    "Wohnfläche": wohnflaeche,
    "Objekttyp": objekttyp,
    "Haustiere erlaubt": haustiere_erlaubt,
    "Balkon / Terrasse": balkon_terrasse,
    "Geschirrspüler": geschirrspueler,
    "Cheminée": cheminee,
    "Kabel-TV": kabel_tv,
    "Aussicht": aussicht,
    "Aussicht auf die Berge": aussicht_berge,
    "Rollstuhlgängig": rollstuhlgaengig,
    "Ruhige Lage": ruhige_lage,
    "Kinderfreundlich": kinderfreundlich,
    "Parkplatz": parkplatz,
    "Garage": garage,
    "Lift": lift,
    "Neubau": neubau,
    "Minergie zertifiziert": minergie_zertifiziert,
    "Minergie Bauweise": minergie_bauweise,
    "Hochparterre": hochparterre
})
    # Periodic save every 10 items
    if len(real_estate_data) % 10 == 0:
        temp_df = pd.DataFrame(real_estate_data)
        temp_df.to_excel("real_estate_data_temporary.xlsx", index=False, engine='openpyxl')
        print("Auto-saved progress at", len(real_estate_data), "entries.")
    driver.get(current_listings_webpage)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ResultListPage_searchBarWrapper_lqBY2"))  # Update this to a unique class or ID on the results page
    )
    next_page = page_number + 1
    print("Proceeding to page " + str(next_page))
    page_link = driver.find_element(By.XPATH, '//a[@aria-label="Zur Seite ' + str(next_page) + '"]')
    page_link.click()
    get_re_data(page_number)
real_estate_data = []
get_re_data(0)

df = pd.DataFrame(real_estate_data)
df.to_excel("real_estate_data.xlsx", index=False, engine='openpyxl')

#first_object_field = WebDriverWait(driver, 10).until(
#        EC.presence_of_element_located((By.XPATH, "//*[@id='app']/main/div/div[2]/div/div/div[5]/div[2]/div[1]/div/a/div/div[1]/div[2]/div[1]/div[1]/div/div[1]/div[1]/ul/li[3]/picture/img"))
#    )
#first_object_field.click()


print('worked')
driver.quit()

#First automatically collect all real estate numbers in a list from the current webpage and then
#let the script find each number, click the corresponding object, collect the relevant variables on the object webpage and then go back to the initial listings page
#In the end it needs to go to the next page and repeat the process until last page
#All data needs to be written onto an .xls


# In[ ]:


#Issue is that always when page refreshes, it somehow skips the part(s) with address etc.


# In[ ]:





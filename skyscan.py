# -*- coding: utf-8 -*-

import requests
import time
import json
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import sys
import os

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    LIGHT_GRAY = '\033[37m'
    DARK_GRAY = '\033[90m'
    BG_BLUE = '\033[44m'
    BG_GREEN = '\033[42m'

OPENSKY_API_URL = "https://opensky-network.org/api/states/all"

TOOL_VERSION = "0.0.1"

current_language = "ar"

MESSAGES = {
    "ar": {
        "welcome": f"{Colors.HEADER}{Colors.BOLD}أهلاً بك في SkyScan - ماسح السماء{Colors.ENDC}",
        "version": f"الإصدار: {TOOL_VERSION}",
        "select_lang": f"{Colors.OKBLUE}اختر لغة الواجهة (ar للعربية, en للإنجليزية): {Colors.ENDC}",
        "invalid_lang": f"{Colors.FAIL}اختيار لغة غير صالح. يرجى إدخال 'ar' أو 'en'.{Colors.ENDC}",
        "auto_detect_location": "هل تريد تحديد موقعك تلقائيًا باستخدام IP؟ (نعم/لا): ",
        "auto_location_success": f"{Colors.OKGREEN}تم تحديد موقعك تلقائيًا:{Colors.ENDC}",
        "auto_location_fail": f"{Colors.WARNING}فشل تحديد الموقع التلقائي من IP. ستحتاج إلى إدخال الإحداثيات يدوياً.{Colors.ENDC}",
        "connection_error": f"{Colors.FAIL}خطأ في الاتصال بالإنترنت أو خدمة تحديد الموقع التلقائي: {Colors.ENDC}",
        "unexpected_error": f"{Colors.FAIL}حدث خطأ غير متوقع أثناء تحديد الموقع التلقائي: {Colors.ENDC}",
        "enter_latitude": f"{Colors.OKBLUE}أدخل خط العرض (Latitude): {Colors.ENDC}",
        "enter_longitude": f"{Colors.OKBLUE}أدخل خط الطول (Longitude): {Colors.ENDC}",
        "invalid_coordinates": f"{Colors.FAIL}إحداثيات غير صالحة. خط العرض يجب أن يكون بين -90 و 90، وخط الطول بين -180 و 180.{Colors.ENDC}",
        "invalid_input_number": f"{Colors.FAIL}إدخال غير صالح. يرجى إدخال أرقام فقط.{Colors.ENDC}",
        "enter_radius": f"{Colors.OKBLUE}أدخل نصف قطر البحث بالكيلومترات (مثال: 100): {Colors.ENDC}",
        "invalid_radius": f"{Colors.FAIL}نصف قطر غير صالح. يرجى إدخال رقم موجب.{Colors.ENDC}",
        "fetching_data": f"{Colors.OKCYAN}جاري جلب بيانات الطائرات...{Colors.ENDC}",
        "no_aircraft_found": f"{Colors.WARNING}لم يتم العثور على طائرات ضمن النطاق المحدد.{Colors.ENDC}",
        "aircraft_details_header": f"{Colors.HEADER}{Colors.BOLD}الطائرات الموجودة ضمن النطاق:{Colors.ENDC}",
        "flight_number": "رقم الرحلة:",
        "origin": "المغادرة:",
        "destination": "الوجهة:",
        "latitude": "خط العرض:",
        "longitude": "خط الطول:",
        "altitude": "الارتفاع:",
        "ground_speed": "السرعة الأرضية:",
        "aircraft_type": "نوع الطائرة:",
        "heading": "الاتجاه:",
        "distance": "المسافة:",
        "meters": "متر",
        "km_h": "كم/ساعة",
        "degree": "درجة",
        "error_fetching_aircraft": f"{Colors.FAIL}خطأ في جلب بيانات الطائرات: {Colors.ENDC}",
        "retrying_in": "إعادة المحاولة خلال",
        "seconds": "ثوانٍ...",
        "press_ctrl_c": f"{Colors.WARNING}{Colors.BOLD}اضغط Ctrl+C للإيقاف.{Colors.ENDC}",
        "exiting": f"{Colors.OKBLUE}جاري الخروج من SkyScan. إلى اللقاء!{Colors.ENDC}",
        "unknown": "غير معروف",
        "current_location_info": f"{Colors.OKGREEN}{Colors.BOLD}معلومات الموقع الحالي ونصف قطر البحث:{Colors.ENDC}",
        "center_point": "نقطة البحث المركزية:",
        "search_radius_label": "نصف قطر البحث:",
        "km_unit": "KM",
        "separator": f"{Colors.DARK_GRAY}="*50 + Colors.ENDC,
        "aircraft_separator": f"{Colors.LIGHT_GRAY}-{Colors.ENDC}"*40,
    },
    "en": {
        "welcome": f"{Colors.HEADER}{Colors.BOLD}Welcome to SkyScan - The Sky Scanner{Colors.ENDC}",
        "version": f"Version: {TOOL_VERSION}",
        "select_lang": f"{Colors.OKBLUE}Select interface language (ar for Arabic, en for English): {Colors.ENDC}",
        "invalid_lang": f"{Colors.FAIL}Invalid language choice. Please enter 'ar' or 'en'.{Colors.ENDC}",
        "auto_detect_location": "Do you want to automatically detect your location using IP? (yes/no): ",
        "auto_location_success": f"{Colors.OKGREEN}Your location detected automatically:{Colors.ENDC}",
        "auto_location_fail": f"{Colors.WARNING}Automatic IP location detection failed. You will need to enter coordinates manually.{Colors.ENDC}",
        "connection_error": f"{Colors.FAIL}Error connecting to the internet or automatic location service: {Colors.ENDC}",
        "unexpected_error": f"{Colors.FAIL}An unexpected error occurred during automatic location detection: {Colors.ENDC}",
        "enter_latitude": f"{Colors.OKBLUE}Enter Latitude: {Colors.ENDC}",
        "enter_longitude": f"{Colors.OKBLUE}Enter Longitude: {Colors.ENDC}",
        "invalid_coordinates": f"{Colors.FAIL}Invalid coordinates. Latitude must be between -90 and 90, and Longitude between -180 and 180.{Colors.ENDC}",
        "invalid_input_number": f"{Colors.FAIL}Invalid input. Please enter numbers only.{Colors.ENDC}",
        "enter_radius": f"{Colors.OKBLUE}Enter search radius in kilometers (e.g., 100): {Colors.ENDC}",
        "invalid_radius": f"{Colors.FAIL}Invalid radius. Please enter a positive number.{Colors.ENDC}",
        "fetching_data": f"{Colors.OKCYAN}Fetching aircraft data...{Colors.ENDC}",
        "no_aircraft_found": f"{Colors.WARNING}No aircraft found within the specified range.{Colors.ENDC}",
        "aircraft_details_header": f"{Colors.HEADER}{Colors.BOLD}Aircrafts within range:{Colors.ENDC}",
        "flight_number": "Flight Number:",
        "origin": "Origin:",
        "destination": "Destination:",
        "latitude": "Latitude:",
        "longitude": "Longitude:",
        "altitude": "Altitude:",
        "ground_speed": "Ground Speed:",
        "aircraft_type": "Aircraft Type:",
        "heading": "Heading:",
        "distance": "Distance:",
        "meters": "meters",
        "km_h": "km/h",
        "degree": "degrees",
        "error_fetching_aircraft": f"{Colors.FAIL}Error fetching aircraft data: {Colors.ENDC}",
        "retrying_in": "Retrying in",
        "seconds": "seconds...",
        "press_ctrl_c": f"{Colors.WARNING}{Colors.BOLD}Press Ctrl+C to stop.{Colors.ENDC}",
        "exiting": f"{Colors.OKBLUE}Exiting SkyScan. Goodbye!{Colors.ENDC}",
        "unknown": "Unknown",
        "current_location_info": f"{Colors.OKGREEN}{Colors.BOLD}Current Location & Search Radius Info:{Colors.ENDC}",
        "center_point": "Center Point:",
        "search_radius_label": "Search Radius:",
        "km_unit": "KM",
        "separator": f"{Colors.DARK_GRAY}="*50 + Colors.ENDC,
        "aircraft_separator": f"{Colors.LIGHT_GRAY}-{Colors.ENDC}"*40,
    }
}

def _(key):
    return MESSAGES[current_language].get(key, key)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def select_language():
    global current_language
    while True:
        lang_choice = input(MESSAGES["ar"]["select_lang"]).strip().lower()
        if lang_choice in ["ar", "en"]:
            current_language = lang_choice
            break
        else:
            print(MESSAGES["ar"]["invalid_lang"])

def get_public_ip_location():
    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=5)
        ip_response.raise_for_status()
        public_ip = ip_response.json()["ip"]

        location_response = requests.get(f"http://ip-api.com/json/{public_ip}", timeout=5)
        location_response.raise_for_status()
        location_data = location_response.json()

        if location_data and location_data.get("status") == "success":
            latitude = location_data.get("lat")
            longitude = location_data.get("lon")
            city = location_data.get("city")
            country = location_data.get("country")
            print(f"{_('auto_location_success')} {city}, {country} ({latitude:.4f}, {longitude:.4f}){Colors.ENDC}")
            return latitude, longitude
        else:
            print(_('auto_location_fail'))
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"{_('connection_error')}{e}{Colors.ENDC}")
        return None, None
    except Exception as e:
        print(f"{_('unexpected_error')}{e}{Colors.ENDC}")
        return None, None

def get_user_coordinates():
    while True:
        try:
            lat = float(input(_('enter_latitude')))
            lon = float(input(_('enter_longitude')))
            if -90 <= lat <= 90 and -180 <= lon <= 180:
                return lat, lon
            else:
                print(_('invalid_coordinates'))
        except ValueError:
            print(_('invalid_input_number'))

def get_search_radius():
    while True:
        try:
            radius = float(input(_('enter_radius')))
            if radius > 0:
                return radius
            else:
                print(_('invalid_radius'))
        except ValueError:
            print(_('invalid_input_number'))

def fetch_aircraft_data(lati, longi, radius):
    lat_delta = radius / 111.0

    try:
        ip_response = requests.get("https://api.ipify.org?format=json", timeout=2)
        ip_response.raise_for_status()
        public_ip = ip_response.json()["ip"]
        location_response = requests.get(f"http://ip-api.com/json/{public_ip}", timeout=2)
        location_response.raise_for_status()
        user_lat_for_lon_calc = location_response.json().get("lat", 1)
    except requests.exceptions.RequestException:
        user_lat_for_lon_calc = 1

    lon_delta = radius / (111.0 * abs(user_lat_for_lon_calc))

    min_latitude = lati - lat_delta
    max_latitude = lati + lat_delta
    min_longitude = longi - lon_delta
    max_longitude = longi + lon_delta

    params = {
        "lamin": min_latitude,
        "lomin": min_longitude,
        "lamax": max_latitude,
        "lomax": max_longitude
    }

    try:
        response = requests.get(OPENSKY_API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("states", [])
    except requests.exceptions.RequestException as e:
        print(f"{_('error_fetching_aircraft')}{e}{Colors.ENDC}")
        return None
    except Exception as e:
        print(f"{_('unexpected_error')}{e}{Colors.ENDC}")
        return None

def display_aircraft_info(aircraft_states, center_coords, search_radius):
    found_aircrafts = []
    for s in aircraft_states:
        if s[6] is not None and s[5] is not None:
            aircraft_coords = (s[6], s[5])
            distance = geodesic(center_coords, aircraft_coords).km

            if distance <= search_radius:
                callsign = s[1].strip() if s[1] else _('unknown')
                latitude = s[6]
                longitude = s[5]
                altitude_meters = s[7] if s[7] is not None else _('unknown')
                ground_speed_mps = s[9] if s[9] is not None else 0
                true_track = s[10] if s[10] is not None else _('unknown')

                ground_speed_kmh = round(ground_speed_mps * 3.6, 2)

                destination = _('unknown')
                aircraft_type = _('unknown')

                found_aircrafts.append({
                    "callsign": callsign,
                    "latitude": latitude,
                    "longitude": longitude,
                    "altitude": altitude_meters,
                    "ground_speed": ground_speed_kmh,
                    "true_track": true_track,
                    "distance": round(distance, 2),
                    "destination": destination,
                    "aircraft_type": aircraft_type
                })

    if not found_aircrafts:
        print(_('no_aircraft_found'))
        return

    print(f"\n{_('aircraft_details_header')}\n")
    for i, ac in enumerate(found_aircrafts):
        print(f"{Colors.OKCYAN}{Colors.BOLD}--- {_('aircraft_type')} {i+1} ---{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('flight_number')}{Colors.ENDC} {Colors.OKBLUE}{ac['callsign']}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('destination')}{Colors.ENDC} {Colors.OKBLUE}{ac['destination']}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('latitude')}{Colors.ENDC} {Colors.OKBLUE}{ac['latitude']:.4f}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('longitude')}{Colors.ENDC} {Colors.OKBLUE}{ac['longitude']:.4f}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('altitude')}{Colors.ENDC} {Colors.OKBLUE}{ac['altitude']} {_('meters')}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('ground_speed')}{Colors.ENDC} {Colors.OKBLUE}{ac['ground_speed']} {_('km_h')}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('heading')}{Colors.ENDC} {Colors.OKBLUE}{ac['true_track']} {_('degree')}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('aircraft_type')}{Colors.ENDC} {Colors.OKBLUE}{ac['aircraft_type']}{Colors.ENDC}")
        print(f"  {Colors.LIGHT_GRAY}{_('distance')}{Colors.ENDC} {Colors.OKBLUE}{ac['distance']} {_('km_unit')}{Colors.ENDC}")
        print(_('aircraft_separator'))

def main():
    clear_screen()
    select_language()

    print(_('welcome'))
    print(_('version'))
    print(_('separator'))

    location_choice = input(_('auto_detect_location')).strip().lower()

    center_latitude, center_longitude = None, None

    if location_choice == _('yes').lower() or location_choice == 'y':
        center_latitude, center_longitude = get_public_ip_location()
        if center_latitude is None:
            print(_('auto_location_fail'))
            center_latitude, center_longitude = get_user_coordinates()
    else:
        center_latitude, center_longitude = get_user_coordinates()

    search_radius = get_search_radius()

    print(f"\n{_('current_location_info')}")
    print(f"  {Colors.OKGREEN}{_('center_point')}{Colors.ENDC} {Colors.OKBLUE}({center_latitude:.4f}, {center_longitude:.4f}){Colors.ENDC}")
    print(f"  {Colors.OKGREEN}{_('search_radius_label')}{Colors.ENDC} {Colors.OKBLUE}{search_radius} {_('km_unit')}{Colors.ENDC}")
    print(_('separator'))
    print(f"\n{_('press_ctrl_c')}\n")

    try:
        while True:
            print(f"\n{_('fetching_data')}")
            aircraft_states = fetch_aircraft_data(center_latitude, center_longitude, search_radius)

            if aircraft_states is not None:
                display_aircraft_info(aircraft_states, (center_latitude, center_longitude), search_radius)

            time.sleep(30)
            clear_screen()
            print(_('welcome'))
            print(_('version'))
            print(_('separator'))
            print(f"\n{_('current_location_info')}")
            print(f"  {Colors.OKGREEN}{_('center_point')}{Colors.ENDC} {Colors.OKBLUE}({center_latitude:.4f}, {center_longitude:.4f}){Colors.ENDC}")
            print(f"  {Colors.OKGREEN}{_('search_radius_label')}{Colors.ENDC} {Colors.OKBLUE}{search_radius} {_('km_unit')}{Colors.ENDC}")
            print(_('separator'))
            print(f"\n{_('press_ctrl_c')}\n")

    except KeyboardInterrupt:
        print(f"\n{_('exiting')}")
    except Exception as e:
        print(f"{Colors.FAIL}حدث خطأ فادح: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()

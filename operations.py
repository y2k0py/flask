from datetime import datetime
import json
import pytz  # Добавьте импорт pytz


def time_now(timezone='Europe/Kiev'):  # Установите часовой пояс по умолчанию, например, для Киева
    now = datetime.now(pytz.timezone(timezone))  # Используйте pytz для установки часового пояса
    date_time = now.strftime("%d.%m.%y %H:%M")
    return date_time


def find_full_region_info(region_name: str):
    try:
        with open('regions.json', 'r') as json_file:
            regions_data = json.load(json_file)
    except FileNotFoundError:
        print("Error: File 'regions.json' not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Unable to decode JSON from 'regions.json'.")
        return None

    region_name_lower = region_name.lower()

    for state in regions_data.get('states', []):
        if state['regionName'].lower().startswith(region_name_lower):
            return state['regionId'], state['regionName']
        for district in state.get('regionChildIds', []):
            if district['regionName'].lower().startswith(region_name_lower):
                return district['regionId'], district['regionName']
            for community in district.get('regionChildIds', []):
                if community['regionName'].lower().startswith(region_name_lower):
                    return community['regionId'], community['regionName']
    return None


def near_region(region_id):
    data = read_json_file('near_regions.json')
    numbers = data.get(str(region_id), [])
    return numbers


def found_near_region(region_id):
    data = read_json_file('near_regions.json')
    numbers = data.get(str(region_id), [])
    return numbers


def read_json_file(file_name):
    try:
        with open(file_name, 'r') as json_file:
            data = json.load(json_file)
        return data
    except FileNotFoundError:
        return print(f'No {file_name} file')


def alert_status(status):
    if status == 'activate':
        return True
    elif status == 'deactivate':
        return False
    else:
        return None


def get_region_name(region_id):
    print('get_region_name')
    data = read_json_file('regions.json')
    for state in data['states']:
        if state['regionId'] == region_id:
            return state['regionName']
        for district in state['regionChildIds']:
            if district['regionId'] == region_id:
                return district['regionName']
            for community in district['regionChildIds']:
                if community['regionId'] == region_id:
                    return community['regionName']


def define_alert_type(alert_type):
    if alert_type == 'UNKNOWN':
        return 'Невідомий рівень тривоги'
    elif alert_type == 'AIR':
        return 'Повітряна тривога'
    elif alert_type == 'ARTILLERY':
        return 'Артилерійська тривога'
    elif alert_type == 'URBAN_FIGHTS':
        return 'Вуличні бої'
    elif alert_type == 'CHEMICAL':
        return 'Хімічний рівень тривоги'
    elif alert_type == 'NUCLEAR':
        return 'Ядерний рівень тривоги'
    elif alert_type == 'INFO':
        return 'Інформаційний рівень тривоги'
    else:
        return 'Unknown alert type'



def find_state_by_region_id(target_region_id):
    if target_region_id is None:
        return None
    json_data = read_json_file("regions.json")
    for state in json_data["states"]:
        for district in state["regionChildIds"]:
            if district["regionId"] == target_region_id:
                return state["regionName"]
            for community in district["regionChildIds"]:
                if community["regionId"] == target_region_id:
                    return state["regionName"]

    return None



def region_is_state(region, r_type='id'):
    if region is None:
        return False
    try:
        if r_type == 'name':
            name = region
        else:
            name = get_region_name(region)
        print(region, r_type)
        if name.split()[-1].lower() == 'область':
            return True
        else:
            return False
    except Exception as e:
        print(f'Помилка, region_is_state: {e}')



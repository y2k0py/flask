from datetime import datetime, time
import json
import pytz  # Добавьте импорт pytz


def time_now(timezone='Europe/Kiev'):  # Установите часовой пояс по умолчанию, например, для Киева
    now = datetime.now(pytz.timezone(timezone))  # Используйте pytz для установки часового пояса
    date_time = now.strftime("%d.%m.%y %H:%M")
    return date_time


def find_full_region_info(region_name: str):
    regions_data = read_json_file('regions.json')

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
        with open(file_name, 'r', encoding="utf-8") as json_file:
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


def time_zone_to_time(time_zone):
    try:
        if time_zone == 815:
            return time(8, 0), time(15, 0)
        elif time_zone == 823:
            return time(8, 0), time(23, 0)
        elif time_zone == 1722:
            return time(17, 0), time(22, 0)
        elif time_zone == 0:
            return time(0, 0), time(23, 59)
    except Exception as e:
        print(f'Помилка, time_zone_to_time: {e}')


def convert_time_from_alert(alert_time):
    try:
        given_time = datetime.strptime(alert_time, '%Y-%m-%dT%H:%M:%SZ')
        given_hours, given_minutes = given_time.hour, given_time.minute
        return [given_hours, given_minutes]
    except Exception as e:
        print(f'Помилка, convert_time_from_alert: {e}')

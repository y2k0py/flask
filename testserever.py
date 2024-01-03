import requests
import json


def send_request():
    # Замени 'http://localhost:5000/webhook' на актуальный URL своего сервера
    webhook_url = 'http://localhost:5000/webhook'

    # Пример данных, которые можно отправить
    data = {'status': 'DEACTIVATE', 'regionId': 18, 'alarmType': 'AIR', 'createdAt': '2024-01-03T19:17:52Z'}

    # Отправляем POST-запрос на сервер
    response = requests.post(webhook_url, json=data)

    # Выводим статус кода ответа сервера
    print(f"Status code: {response.status_code}")


# Вызываем функцию для отправки запроса
send_request()

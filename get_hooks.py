from flask import Flask, request, jsonify
import requests
from config import API_BOT_TOKEN, API_UKRAINE_ALARM_KEY, WEBHOOK_URL, SUBSCRIPTION_URL
import db
import json
import os
from operations import alert_status, define_alert_type, found_near_region, get_region_name

app = Flask(__name__)

webhook_url = "/webhook"


def subscribe_to_webhook():
    payload = {
        "webHookUrl": WEBHOOK_URL
    }
    headers = {
        "Content-Type": "application/json",
        "accept": "text/plain",
        "Authorization": API_UKRAINE_ALARM_KEY
    }
    response = requests.post(SUBSCRIPTION_URL, json=payload, headers=headers)
    print("Subscription Status Code:", response.status_code)
    if response.status_code == 200:
        print("Successfully subscribed to the webhook")
    else:
        print("Failed to subscribe to the webhook")



@app.route(webhook_url, methods=['POST', 'GET'])
def webhook_handler():
    try:
        data = request.get_data().decode("utf-8")  # Получаем данные от вебхука в виде строки
        data_dict = json.loads(data)  # Преобразуем строку в словарь
        print("Received webhook data:", data_dict)
        send_main_region_alert(data_dict)
        send_alert_from_near_region(data_dict)
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Error processing webhook data: {str(e)}")
        return jsonify({"status": "error"})


def send_main_region_alert(received_alert):
    users = db.get_all_users()
    for user in users:
        if user['region_id'] == str(received_alert['regionId']):
            user_id = user['telegram_id']
            if alert_status(received_alert['status'].lower()):
                text = f"🔴 Увага! В вашому регіоні {(define_alert_type(str(received_alert['alertType'])).lower())}!"
            else:
                text = f"🟢 Відбій тривоги в вашому регіоні!"
            send_message(user_id, text)
        else:
            print('User not in this region')
            print(received_alert['regionId'] + ' ' + str(user['region_id']))


def send_alert_from_near_region(received_alert):
    users = db.get_near_region_turned_on()
    for user in users:
        print(user)
        nearby_regions = found_near_region(user['region_id'])
        print(nearby_regions)
        if int(received_alert['regionId']) in nearby_regions:
            print('Alert in near region')
            user_id = user['telegram_id']
            if not alert_status(received_alert['status'].lower()):
                text = f"🟢 Відбій тривоги в '{get_region_name(received_alert['regionId'])}', регіоні біля вас!"
            else:
                text = f"🔴 Увага! В '{get_region_name(received_alert['regionId'])}', біля вас - {(define_alert_type(str(received_alert['alertType'])).lower())}!"
            send_message(user_id, text)


def send_message(user_id, text):
    bot_url = f'https://api.telegram.org/bot{API_BOT_TOKEN}'
    url = f'{bot_url}/sendMessage?chat_id={user_id}&text={text}'
    response = requests.get(url)
    print(response)


# TODO сделать так если у меня установлен область то регионы по близости работали, а если нет то не работали
#       перетащить некоторые функции в db.py и некоторые в отдельный файл


if __name__ == "__main__":
    subscribe_to_webhook()
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv("PORT", default=5000)))


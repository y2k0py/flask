from flask import Flask, request, jsonify
import requests
from config import API_BOT_TOKEN, API_UKRAINE_ALARM_KEY, WEBHOOK_URL, SUBSCRIPTION_URL
import db
import os
from operations import *
import threading

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


@app.route(webhook_url, methods=['POST'])
def webhook_handler():
    try:
        data = request.get_data().decode("utf-8")  # Получаем данные от вебхука в виде строки
        data_dict = json.loads(data)  # Преобразуем строку в словарь
        print("Received webhook data:", data_dict)
        send_alerts(data_dict)
        return jsonify({"status": "success"})
    except Exception as e:
        app.logger.error(f"Error processing webhook data: {str(e)}")
        return jsonify({"status": "error"})


def send_alerts(received_alert):
    users = db.get_all_users()
    time_from_alert = convert_time_from_alert(received_alert['createdAt'])
    threads = []

    for user in users:

        time_zone = time_zone_to_time(user['time_zone'])
        if user['notifications']:
            if time_zone[0] <= time(time_from_alert[0], time_from_alert[1]) <= time_zone[1]:
                # Создаем поток для отправки уведомлений пользователю и добавляем его в список потоков
                thread = threading.Thread(target=send_user_alert, args=(received_alert, user))
                threads.append(thread)
                # Запускаем поток
                thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()


def send_user_alert(received_alert, user):
    # Отправляем уведомление о главном регионе
    send_main_region_alert(received_alert, user)

    # Отправляем уведомление о дополнительном регионе
    send_additional_region_alert(received_alert, user)

    # Отправляем уведомление о близком регионе
    send_alert_from_near_region(received_alert, user)


def send_main_region_alert(received_alert, user):
    # Определяем ID пользователя и текст сообщения
    user_id = user['telegram_id']
    if user['region_id'] == str(received_alert['regionId']):
        text = generate_alert_text(received_alert, is_main_region=True)
        send_message(user_id, text)


def send_additional_region_alert(received_alert, user):
    # Определяем ID пользователя и текст сообщения
    user_id = user['telegram_id']
    if user['additional_region'] == str(received_alert['regionId']):
        text = generate_alert_text(received_alert, is_main_region=False)
        send_message(user_id, text)


def send_alert_from_near_region(received_alert, user):
    # Получаем близлежащие регионы пользователя
    nearby_regions = found_near_region(user['region_id'])

    # Проверяем, находится ли регион уведомления среди близлежащих
    if int(received_alert['regionId']) in nearby_regions:
        # Определяем ID пользователя и текст сообщения
        user_id = user['telegram_id']
        text = generate_alert_text(received_alert, is_main_region=False, is_nearby=True)
        send_message(user_id, text)


def change_gender(region_name):
    if region_name is not None:
        if region_name.endswith('ська область'):
            return region_name.replace('ська область', 'ській області')
        elif region_name.endswith('зька область'):
            return region_name.replace('зька область', 'зькій області')
        else:
            return region_name


def generate_alert_text(received_alert, is_main_region=False, is_nearby=False):
    # Генерируем текст уведомления в зависимости от типа и статуса уведомления
    if alert_status(received_alert['status'].lower()):
        prefix = f"🔴 Увага! {(define_alert_type(str(received_alert['alarmType'])))} 🔴"
    else:
        prefix = "🟢 Відбій тривоги 🟢"

    if is_nearby:
        region_name = get_region_name(str(received_alert['regionId']))
        formated_region_name = change_gender(region_name)
        return f"{prefix}\n🌍 В {formated_region_name}, біля вас!"
    elif is_main_region:
        return f"{prefix}\n🌍 В вашій області!"
    else:
        return f"{prefix}\n🌍 В додатковій області!"


def send_message(user_id, text):
    # Отправляем сообщение через Telegram API
    bot_url = f'https://api.telegram.org/bot{API_BOT_TOKEN}'
    url = f'{bot_url}/sendMessage?chat_id={user_id}&text={text}'
    response = requests.get(url)
    print(f'Status code of sending message to user: {response.status_code}')


if __name__ == "__main__":
    from waitress import serve

    subscribe_to_webhook()
    serve(app, host='0.0.0.0', port=int(os.getenv("PORT", default=5000)))

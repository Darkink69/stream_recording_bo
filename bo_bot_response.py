import requests
import json
import time
import datetime as dt
from datetime import datetime
import uni_telegram_bot
import main_bo

TOKEN = "6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q"
URL = 'https://api.telegram.org/bot'


def time_now():
    return dt.datetime.now().strftime("%D %H:%M:%S")


def timestamp_to_date(tmstmp):
    objectdate = datetime.fromtimestamp(tmstmp)
    return objectdate


def get_updates(offset=0):
    messages = requests.get(f'{URL}{TOKEN}/getUpdates?offset={offset}').json()
    return messages


def reply_keyboard(chat_id, text):
    reply_markup = {"keyboard": [["Первая на странице"], ["Скачать плейлист со всеми трансляциями"], ["Топ-10 на странице"]], "resize_keyboard": True, "one_time_keyboard": True}
    data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_markup)}
    requests.post(f'{URL}{TOKEN}/sendMessage', data=data)


def add_to_json(messages):
    for message in messages['result']:
        chat_id = message['message']['chat']['id']
        first_name = message['message']['chat']['first_name']
        try:
            username = message['message']['chat']['username']
        except BaseException:
            username = ''
        date = str(timestamp_to_date(message['message']['date']))
        text = message['message']['text']

        data = json.load(open("db_users_bo.json", "r", encoding='utf-8'))

        all_ids = []
        for id in data:
            all_ids.append(id['id'])

        if chat_id not in all_ids:
            print(f'{time_now()} | Боту написал новый пользователь {first_name}, {username}, id {chat_id}.')
            json_data = {
                "id": chat_id,
                "first_name": first_name,
                "username": username,
                "premium": True,
                "requests": [
                    [
                        {"date": date},
                        {"text": text}
                    ]
                ]
            }
            data.append(json_data)
            with open("db_users_bo.json", "w", encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)


def check_message(chat_id, message, date):
    print(f'{time_now()} | Пользователь с id {chat_id} написал боту: "{message}".')
    if message.lower() in ['первая на странице', 'первая']:
        profiles = main_bo.get_profiles()
        profile = main_bo.get_first_profile(profiles)

        info_profile, stream_full, stream_low, url_stream = main_bo.get_info_profile(profiles, profile)
        img_url, message = main_bo.make_message(info_profile, stream_full, stream_low, url_stream)
        uni_telegram_bot.send_photo_url(chat_id, img_url)
        uni_telegram_bot.send_message(chat_id, message)

    elif message.lower() in ['случайная', 'rnd', 'random']:
        profiles = main_bo.get_profiles()
        profile = main_bo.get_random_profile(profiles)

        info_profile, stream_full, stream_low, url_stream = main_bo.get_info_profile(profiles, profile)
        img_url, message = main_bo.make_message(info_profile, stream_full, stream_low, url_stream)
        uni_telegram_bot.send_photo_url(chat_id, img_url)
        uni_telegram_bot.send_message(chat_id, message)

    elif message.lower().split(' ')[0] in ['record', 'rec', 'запись']:
        print(message, 'это прислали..')
        name = message.split(' ')[1]
        print(name)
        main_bo.start_record(name)
        # profile = main_bo.get_random_profile(profiles)
        #
        # info_profile, stream_full, stream_low, url_stream = main_bo.get_info_profile(profiles, profile)
        # img_url, message = main_bo.make_message(info_profile, stream_full, stream_low, url_stream)
        # uni_telegram_bot.send_photo_url(chat_id, img_url)
        # uni_telegram_bot.send_message(chat_id, message)

    elif message.lower() in ['скачать плейлист со всеми трансляциями', 'play', 'playlist', 'плейлист', 'плэйлист']:
        profiles = main_bo.get_profiles()
        doc = main_bo.make_playlist_m3u8(profiles)
        uni_telegram_bot.send_document(chat_id, doc)

    elif message.lower() in ['топ-10 на странице', '10']:
        profiles = main_bo.get_profiles()
        top_ten = main_bo.get_top_ten(profiles)

        # info_profile, stream_full, stream_low, url_stream = main_bo.get_info_profile(profiles, profile)
        # img_url, message = main_bo.make_message(info_profile, stream_full, stream_low, url_stream)
        # uni_telegram_bot.send_photo_url(chat_id, img_url)
        uni_telegram_bot.send_message(chat_id, top_ten)

    elif message.lower() in ['количество пользователей', 'users']:
        data_users = json.load(open("db_users_bo.json", "r", encoding='utf-8'))
        users = []
        for i in data_users:
            users.append(i['first_name'])
        message = f'{len(data_users)} пользователей(ля) бота\n' \
                  f'{users}\n'

        uni_telegram_bot.send_message(chat_id, message)

    elif message.lower() in ['/start']:
        info = f'Приветствую вас!\n' \
               f'Я бот, который позволяет смотреть BongaCams прямо тут. Введите имя модели или воспользуйтесь готовыми запросами.\n' \
               f'Плейлисты удобнее всего смотреть в приложении VLC-player или другом аналогичном.' \

        uni_telegram_bot.send_message(chat_id, info)
        reply_keyboard(chat_id, '!!!')

    else:
        print(message, 'это прислали..')
        # name = message
        # profiles = main_bo.get_profiles()
        # profile = main_bo.get_info_profile(profiles, name)
        # print(info_profile, stream_full, stream_low, url_stream, '!!!!!!!!!!!')
        # info_profile, stream_full, stream_low, url_stream = main_bo.get_info_profile(profiles, profile)
        # img_url, message = main_bo.make_message(info_profile, stream_full, stream_low, url_stream)
        # uni_telegram_bot.send_photo_url(chat_id, img_url)
        # uni_telegram_bot.send_message(chat_id, message)
        reply_keyboard(chat_id, 'Поиск по конкретному имени пока не работает ;(')


def run():
    print(f'{time_now()} | Сервер бота запущен.')
    update_id = get_updates()['result'][-1]['update_id']  # Присваиваем ID последнего отправленного сообщения боту
    # update_id = 951251229
    while True:
        time.sleep(180)
        messages = get_updates(update_id)  # Получаем обновления
        for message in messages['result']:
            # Если в обновлении есть ID больше чем ID последнего сообщения, значит пришло новое сообщение
            if update_id < message['update_id']:
                update_id = message['update_id']  # Присваиваем ID последнего отправленного сообщения боту
                # Отвечаем тому кто прислал сообщение боту
                check_message(message['message']['chat']['id'], message['message']['text'], message['message']['date'])
                add_to_json(messages)


if __name__ == '__main__':
    run()




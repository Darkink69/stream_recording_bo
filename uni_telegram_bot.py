import requests
import json

TOKEN = "6082546372:AAHM33fkvArJpe8wU5IQeg0L4jOGNpHJe2Q"
# chat_id = "813012401"
URL = 'https://api.telegram.org/bot'


def send_message(chat_id, message):
    requests.get(f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={message}&parse_mode=html&disable_web_page_preview=true')


def send_photo_file(chat_id, img):
    files = {'photo': open(img, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}', files=files)


def send_document(chat_id, doc):
    # document = open('tests/test.zip', 'rb'))
    with open(doc, 'rb') as f:
        files = {'document': f}
        requests.post(f'{URL}{TOKEN}/sendDocument?chat_id={chat_id}', files=files)


def send_photo_url(chat_id, img_url):
    # print(img_url)
    requests.get(f'{URL}{TOKEN}/sendPhoto?chat_id={chat_id}&photo={img_url}')


def send_video_file(chat_id, video):
    files = {'video': open(video, 'rb')}
    requests.post(f'{URL}{TOKEN}/sendVideo?chat_id={chat_id}', files=files)









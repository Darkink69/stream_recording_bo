import time
import datetime
import math
import datetime as dt
import subprocess
import json
import os
import requests
from fake_useragent import UserAgent
import yt_dlp
import random

url_stream = 'https://ru2.bongacams16.com/'
all_names = ["jucieLussie", "Taanni", "marina4love", "princess-dia", "lisfoster", "crazypussy07", "miladystarlig",
             "sexparaa", "karamelkkka", "redfury69", "daenerysdaen", "-VikkiL0vesCheese-", "MissFentasy1",
             "ReginaHawk", "Ellis-Walker"]

html_tags_body = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="UTF-8" />\n<link rel="icon" '
                  'Все события города">\n<title>ГдеЧто</title>\n</head>\n<body>\n')
html_tags_main = '<div class="flex-container">\n'
html_tags_main_close = f'</div>\n'
html_tags_close = '</body>\n</html>\n'
html_styles = '<style>\n.flex-container {\ndisplay: flex;\njustify-content: center;\nflex-wrap: wrap;\n}\n.item {\npadding: 1.5rem;\n}\n</style>\n'

def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")

for i in range(10000):
    event_content = ""
    text_file = open(f"events.html", "w", encoding='utf-8')
    ct = datetime.datetime.now()
    ts = ct.timestamp()

    for name in all_names:
        folder = f"names/{name}"
        if not os.path.isdir(folder):
            os.mkdir(folder)
        download_json = f'yt-dlp -P {folder} {url_stream}{name} --write-info-json --skip-download'

        try:
            subprocess.run(download_json, shell=True, stdin=None, stderr=subprocess.PIPE)
            files = os.listdir(folder)
            if len(files) != 0:
                for file in files:
                    if file[-4:] == 'json':
                        print(time_now(), '| Online!')
                        data = json.load(open(f"{folder}/{file}", "r", encoding='utf-8'))
                        print(data['id'])

                        live = data['formats'][0]['manifest_url']
                        print(live)

                        edge = data['formats'][0]['manifest_url'].split('/')[2].split('.')[0].split('-')[1]
                        mobile_img = f'https://mobile-{edge}.bcvcdn.com/stream_{data["uploader_id"]}.jpg'
                        print(mobile_img)
                        headers = {"User-Agent": UserAgent().random}
                        r = requests.get(mobile_img, headers=headers)
                        with open(f'{folder}/{name}_{math.ceil(ts)}.jpg', 'wb') as img:
                            img.write(r.content)

                        # print(math.ceil(ts))
                        video_thumb = f'https://vthumb{edge[-2:]}.bcvcdn.com/stream_{data["uploader_id"]}.mp4?t={math.ceil(ts)}'
                        print(video_thumb)
                        headers = {"User-Agent": UserAgent().random}
                        r = requests.get(video_thumb, headers=headers)
                        with open(f'{folder}/{name}_{math.ceil(ts)}.mp4', 'wb') as video:
                            video.write(r.content)

                        my_file = open(f"{folder}/{data['id']}_{edge}.m3u8", "w+")
                        text = f"#EXTM3U\n#EXTINF:10.0, {data['id']}\n{data['formats'][0]['manifest_url']}"
                        my_file.write(text)
                        my_file.close()

                        content = (
                                   f'<div class="item">\n'
                                   f'<img src="{mobile_img}">\n'
                                   # f'<video controls="" autoplay="" name="media">\n'
                                   # f'<source src="{video_thumb}" type="video/mp4">\n'
                                   # f'</video>\n'
                                   
                                   f'<p>{name}</p>\n'
                                   f'</div>\n'
                                   )

                        event_content += content
                    os.remove(f"{folder}/{file}")

            else:
                print(time_now(), '| Offline')

            print(time_now(), '| Не удалось подключиться.. ')
        except BaseException:
            print(time_now(), '| Какая-то ошибка..')

    all_content = f"{html_tags_body}{html_styles}{html_tags_main}{event_content}{html_tags_main_close}{html_tags_close}"
    text_file.write(str(all_content))
    text_file.close()
    print("Подождем часок...")

    time.sleep(3600)



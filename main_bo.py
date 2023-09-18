import time
import datetime as dt
import json
import yt_dlp
import random
import parse_bo
import rec_bo
import yt_dlp_info
import uni_telegram_bot


# chat_id = "813012401"
def get_profiles():
    profiles = parse_bo.get_bonga_profiles()
    return profiles


def get_item_profile():
    profile = 'Taanni'
    # 'https://mobile-edge34.bcvcdn.com/stream_Taanni.jpg'
    return profile


def get_random_profile(profiles):
    profile = profiles[random.randrange(len(profiles))]['name']
    return profile


def get_first_profile(profiles):
    profile = profiles[0]['href']
    return profile


def get_last_profile(profiles):
    profile = profiles[-1]['name']
    return profile


def get_4kcam_profile(profiles):
    pass
    # for i in profiles:
    #     if i['video'].split('x')[1] == '1080':
    #         print(i)
    #     else:
    #         print('Нету')


def get_max_viewers_profile(profiles):
    pass
    # max_viewers = max(viewers)
    # max_index = viewers.index(max_viewers)


def start_record(name):
    url_stream = f'https://rus.bongacams16.com/{name}'
    rec_bo.record(url_stream)


def get_top_ten(profiles):
    top_ten = []
    for i in range(10):
        top_ten.append(profiles[i]['name'])
    return top_ten


def get_phone_profile(profiles):
    pass


def make_playlist_m3u8(profiles):
    my_file = open("playlist.m3u8", "w+")
    my_file.write(f"#EXTM3U\n")
    for i in profiles:
        text = f"#EXTINF:10.0, {i['name']}\n{i['stream_full']}\n"
        my_file.write(text)
    my_file.close()
    return "playlist.m3u8"


def get_info_profile(profiles, profile):
    info_profile = profiles[0]
    for i in profiles:
        if i['href'] == profile:
            print(i)
            info_profile = i
            stream_full = i['stream_full']
            stream_low = i['stream_low']

    url_stream = f"https://rus.bongacams16.com/{profile}"
    print(url_stream)


    # try:
    #     data_stream = yt_dlp_info.get_info_dlp(url_stream)
    # except BaseException:
    #     print('Не удалось получить ссылку на трансляцию')

    # print(data_stream)
    # try:
    #     stream_full = data_stream['formats'][-1]['url']
    #     stream_low = data_stream['formats'][0]['url']
    # except BaseException:
    #     stream_full = False
    #     stream_low = False

    return info_profile, stream_full, stream_low, url_stream


def make_message(info_profile, stream_full, stream_low, url_stream):
    print(info_profile)
    img_url = info_profile['img']

    strm_low = f"<a href='{stream_low}'>НИЗКОЕ КАЧЕСТВО</a>"
    strm_high = f"<a href='{stream_full}'>МАКСИМАЛЬНОЕ ({info_profile['video']})</a>"
    message = f"<strong>{info_profile['name']}</strong>\n" \
              f"<a href='{info_profile['img_live']}'>ОБНОВИТЬ КАРТИНКУ</a>\n" \
              f"Зрителей: {info_profile['viewers']}\n" \
              f"Язык: {' Русский.' if info_profile['ru'] else ' Не русский.'}" \
              f"{' Cъемка со смартфона.' if info_profile['mobile'] else ''}" \
              f"{'<b> Впервые в эфире!</b>' if info_profile['new'] else ''}\n\n" \
              f"{'Ссылки на трансляцию:' if stream_low != False else '<i>Модель оффлайн или в привате :(</i>'}\n" \
              f"{strm_low if stream_low != False else ''}\n\n" \
              f"{strm_high if stream_low != False else ''}\n" \
              f"Ссылка на страницу:\n" \
              f"<span class='tg-spoiler'>{url_stream}</span>"
    return img_url, message


# for i in range(10000):
# profile = get_random_profile(profiles)
# profile = get_item_profile()
# profile = get_first_profile(profiles)
# profile = get_last_profile(profiles)

# info_profile, stream_full, stream_low, url_stream = get_info_profile(profiles, profile)


# img_url, message = make_message(info_profile, stream_full, stream_low, url_stream)
# uni_telegram_bot.send_photo_url(chat_id, img_url)
# uni_telegram_bot.send_message(chat_id, message)
    # time.sleep(7200)


# http://live-edge17.bcvcdn.com/hls/stream_Taanni/public-aac/stream_Taanni/chunks.m3u8
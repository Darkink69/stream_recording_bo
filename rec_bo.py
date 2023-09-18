import time
import datetime as dt
import subprocess
import signal
import os
import psutil
import yt_dlp


# url_stream = 'https://www.youtube.com/live/hg4jV_kXw68'
# url_stream = 'https://rus.bongacams16.com/redfury69'
# url_stream = 'https://rus.bongacams16.com/pasha0864'
# url_stream = 'https://rus.bongacams16.com/taanni'


def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")


def record(url_stream):
    folder = url_stream.split('/')[-1]
    if not os.path.isdir(folder):
        os.mkdir(folder)

    pro = f'yt-dlp -P {folder} {url_stream}'
    print(time_now(), f'| Попытка подключения')

    try:
        pr = subprocess.run(pro, shell=True, stdin=None, stderr=subprocess.PIPE)
    except BaseException:
        print(time_now(), '| Не удалось подключиться.. ')



# record(url_stream)
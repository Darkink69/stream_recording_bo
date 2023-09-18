import time
import datetime as dt
import subprocess
import signal
import os
import psutil
import yt_dlp
import random
import parse_bo



# url_stream = 'https://www.youtube.com/live/hg4jV_kXw68'
# url_stream = 'https://rus.bongacams16.com/redfury69'
url_stream = 'https://rus.bongacams16.com/pasha0864'
# url_stream = 'https://rus.bongacams16.com/taanni'
attempt = 0


folder = url_stream.split('/')[-1]
if not os.path.isdir(folder):
    os.mkdir(folder)


def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")


def record(url_stream, attempt=0):
    pro = f'yt-dlp -P {folder} {url_stream}'


    print(time_now(), f'| Попытка подключения')

    try:
        pr = subprocess.run(pro, shell=True, stdin=None, stderr=subprocess.PIPE)
        attempt = 0
    except BaseException:
        print(time_now(), '| Не удалось подключиться.. ')
        attempt += 1




for i in range(10000):
    pro = f'yt-dlp -P {folder} {url_stream}'

    print('цикл', i, '-----------------------------------------------')
    wait_sec = [0, 300, 600, 1800, 3600, 7200, 14400, 24800]
    if attempt > 6:
        attempt = 0

    # record(url_stream, attempt)
    print(time_now(), f'| Попытка подключения')

    try:
        pr = subprocess.run(pro, shell=True, stdin=None, stderr=subprocess.PIPE)
        attempt += 1
        print(time_now(), '| Не удалось подключиться.. ')
        print(time_now(), '| Подождем', wait_sec[attempt], 'секунд')
    except BaseException:
        attempt = 0
        print(time_now(), '| Какая-то ошибка..')

    print(attempt)

    time.sleep(wait_sec[attempt])









# process_call_str = 'yt-dlp "ytsearch3:angelina joly" --get-id --get-title'
# output = subprocess.check_output(process_call_str, shell=True)
# print(output)
#
# # time.sleep(10)
# process_call_str.terminate()
# print('конец')

# n = 5
#
# # Open a text file on write mode (w)
# with open("out.txt", "w+") as f:
#     for i in range(n):
#         # loop n times and write the
#         # loop index to the file
#         # each number in a new line
#         f.write(str(i) + "\n")
#         # sleep for 10 seconds
#         time.sleep(3)

# execute another Python script in subprocess

# process_call_str = 'yt-dlp "ytsearch3:angelina joly" --get-id --get-title'
# output = subprocess.check_output(process_call_str, shell=True)
# print(output)


# for proc in psutil.process_iter():
#     print(proc)
#     if proc.name() == 'conhost.exe':
#         # proc.terminate()
#         proc.send_signal(signal.CTRL_C_EVENT)

# pro.kill()
# def handler(x):
#     pass
#
# os.kill(signal.CTRL_C_EVENT)

# pro.stdin.flush()
# pro.send_signal(signal.CTRL_BREAK_EVENT)
# os.killpg(os.getpgid(pro.pid), signal.SIGTERM)



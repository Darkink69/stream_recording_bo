import json
import yt_dlp


def get_info_dlp(url_stream):

    ydl_opts = {'cookies-from-browser': 'chrome'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_stream, download=False)
        # print(info)
        return info


# url_stream = 'https://rus.bongacams16.com/Taanni'
# get_info_dlp(url_stream)
# '--cookies-from-browser chrome'


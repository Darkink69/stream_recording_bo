from selenium import webdriver
from selenium.webdriver.common.by import By
# import time
import json
import requests


def get_bonga_profiles():
    urls = ['https://rus.bongacams16.com/', 'https://rus.bongacams16.com/couples', 'https://rus.bongacams16.com/new-models']
    profiles = []
    for url in urls:
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        driver = webdriver.Chrome(options)
        driver.get(url)
        elements = driver.find_elements(By.CLASS_NAME, 'ls_thumb')
        for e in elements:
            profile = e.get_attribute("outerHTML")
            # print(profile)
            name = profile[profile.find('title="') + 7:profile.find(' профиль')]
            href = profile[profile.find('/profile/') + 9:profile.find('" title=')]
            video = profile[profile.find('data-vq="') + 9:profile.find('" data-esid=')]
            img = 'https://' + profile[profile.find('img src="//') + 11:profile.find('" alt=')]
            img_live = f'https://mobile-{profile[profile.find("data-esid=") + 16:profile.find("><span class=") - 1]}.bcvcdn.com/stream_{name}.jpg'
            live = True if '__live' in profile else False
            ru = True if '__l_russian' in profile else False
            mobile = True if '__mobile' in profile else False
            vibratoy = True if '__vibratoy' in profile else False
            new = True if '__new' in profile else False
            viewers = int(profile.split('lst_viewers">')[-1].split('</div></div>')[0])
            url_stream_low = f"http://{profile[profile.find('data-esid=') + 11:profile.find('><span class=') - 1]}.bcvcdn.com/hls/stream_{name}/public-aac/stream_{name}_240/chunks.m3u8"
            url_stream_full = f"http://{profile[profile.find('data-esid=') + 11:profile.find('><span class=') - 1]}.bcvcdn.com/hls/stream_{name}/public-aac/stream_{name}/chunks.m3u8"

            json_data = {
                "name": name,
                "href": href,
                "video": video,
                "img": img,
                "img_live": img_live,
                "live": live,
                "ru": ru,
                "mobile": mobile,
                "vibratoy": vibratoy,
                "new": new,
                "viewers": viewers,
                "stream_low": url_stream_low,
                "stream_full": url_stream_full
            }
            # print(json_data)
            profiles.append(json_data)

    return profiles



# get_bonga_profiles()

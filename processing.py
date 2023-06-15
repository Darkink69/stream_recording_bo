import time
import datetime as dt
import subprocess
import signal
import os
import psutil
import yt_dlp
from ffprobe import FFProbe
import math
import nsfw

folder = 'taanni'
scan_sec = 15
wait_different = 60


def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")


def get_video_info(folder, file):
    metadata = FFProbe(f'{folder}/{file}')
    # print(metadata)
    for stream in metadata.streams:
        print(stream)
        if stream.is_video():
            # print(stream.frame_size())
            # print(stream.duration_seconds())
            # w = stream.frame_size()[0] // 10
            # h = stream.frame_size()[1] // 10
            # tile_h = math.ceil(stream.duration_seconds() / 20)
            # if tile_h < 1:
            #     tile_h = 1
            duration = stream.duration_seconds()
        elif stream.is_audio():
            duration = stream.duration_seconds()

            return duration


def get_name_files(folder):
    files_dir = os.listdir(folder)
    files_video = []
    for file in files_dir:
        if os.path.isfile(f'{folder}/{file}'):
            new_name = file.replace(' ', '_')
            os.rename(f'{folder}/{file}', f'{folder}/{new_name}')
            files_video.append(new_name)

    print(f'В папке {folder} - {len(files_video)} файла(ов)')
    return files_video


def make_screens(folder, file):
    print(folder, file)
    if not os.path.isdir(f'{folder}/{file[:-5]}'):
        path = f'{os.getcwd()}\\{folder}/' + file[:-5]
        os.mkdir(path)

        fps = 1 / scan_sec
        print(fps)

        try:
            pro = f'ffmpeg -i {folder}/{file} -r {fps} {folder}/{file[:-5]}/frame_%03d.jpg'
            pr = subprocess.check_call(pro, shell=True)
        except BaseException:
            print(time_now(), 'Ошибка создания картинок')


def make_frames_info(folder, file, results_nsfw_all):
    try:
        os.remove(f"{folder}/{file[:-5]}/frame_001.jpg")
    except BaseException:
        pass
    files_in_folder = os.listdir(f'{folder}/{file[:-5]}')
    duration = get_video_info(folder, file)
    print(duration)
    print(len(files_in_folder))
    print(files_in_folder)

    print(duration // len(files_in_folder), 'каждые секунд')
    print(scan_sec, 'реально задано')
    real_fps_sec = int(duration // len(files_in_folder))
    print(real_fps_sec)

    frames_info = {}
    h, m, s = 0, 0, 0
    for file in files_in_folder:
        time_frame = f'{h}:{m}:{s}'
        print(time_frame)

        frames_info[file] = {'time': time_frame, 'nsfw': False, 'face': False}

        s += scan_sec
        if s > 59:
            m += 1
            s = s - 60
        if m > 59:
            h += 1
            m = m - 60

        if file in results_nsfw_all:
            frames_info[file]['nsfw'] = True

    return frames_info


def cut_video(folder, file, frames_info):
    print(time_now(), f'| Создание короткой версии файла')

    names_cut_videos = []
    for k, v in frames_info.items():
        if v["nsfw"]:
            pro = f'ffmpeg -ss {v["time"]} -i {folder}/{file} -c copy -t 00:00:{scan_sec} {folder}/cut_{k[:-4]}.mp4'
            pr = subprocess.check_call(pro, shell=True)
            name_cut_video = f'file cut_{k[:-4]}.mp4'
            names_cut_videos.append(name_cut_video)

    print(names_cut_videos)
    with open(f"{folder}/concat.txt", "w") as file:
        for i in names_cut_videos:
            file.write(i + '\n')

    pro = f'ffmpeg -f concat -i {folder}/concat.txt -c copy {folder}/SHORT.mp4'
    pr = subprocess.check_call(pro, shell=True)

    try:
        with open(f"{folder}/concat.txt", "r") as file:
            for i in file:
                # print(i.strip().split(' ')[1])
                delete = i.strip().split(' ')[1]
                os.remove(f"{folder}/{delete}")

        os.remove(f"{folder}/concat.txt")
    except BaseException:
        pass


def process_files(folder, files):
    for file in files:
        # try:
        print(time_now(), f'| обрабатывается папка - {folder}, видео - {file}')

        make_screens(folder, file)

        path_folder = f'{folder}/{file[:-5]}'
        results_nsfw_all = nsfw.get_nsfw_frames(path_folder)
        print(time_now(), '| Кадров, содержащих nsfw -', len(results_nsfw_all))
        print(results_nsfw_all)

        # results_nsfw_all = []

        frames_info = make_frames_info(folder, file, results_nsfw_all)
        print(frames_info)
        print(len(frames_info))

        # all_cut_video = cut_video(folder, file, frames_info)
        # print(all_cut_video)

        # print(time_now(), f'| {file} успешно обработан')
        # except BaseException:
        #     print('Ошибка с файлом', file)


print(time_now(), '| начало обработки')

files = get_name_files(folder)
print(files)
process_files(folder, files)

# file = 'Taanni_2023-04-11_17_07_[taanni].mp4'


print(time_now(), '| обработка завершена')

# pr = subprocess.run(pro, shell=True, stdin=None, stderr=subprocess.PIPE)
# ffmpeg -i 1.mp4 -r 0.01 output_%04d.jpg
# ffmpeg -ss 01:01:43 -i 1.mp4 -c copy -t 00:01:08  cut_1_test.mp4

# concat.txt
# file Video-01.mp4
# file Video-02.mp4
# file Video-03.mp4

# ffmpeg -f concat -i concat.txt -c copy output.mp4

# ffmpeg -i 2.mp4 -i metadata -map_metadata 1 MyVideo_1.mp4  # долго, потому что пережимает


# pro = f'ffmpeg -i {folder}/{file} -vf select="eq(pict_type\,PICT_TYPE_I)",scale={w}:{h},tile={tile_w}x{tile_h} -frames:v 1 -y {folder}/{file}.jpg'
# pr = subprocess.check_call(pro, shell=True)

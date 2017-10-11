
import time
import math
import requests
import traceback
import datetime
from progressbar import ProgressBar

__version__ = '1.0.5'
client_id = "<CLIENT_ID>"


def convert_url_to_file_path(url):
    file_name = url.split("/")[-1].replace(".jpg", "") + str(math.floor(time.time()))
    file_path = "images/{0}.jpg".format(file_name)
    return file_path


def download_image(image_url, image_path):
    with open(image_path, "wb") as output_file:
        content = requests.get(image_url).content
        output_file.write(content)


def send_request(url):
    user_agent = 'python-requests/{requests_ver} ttvsnap/{this_ver}'.format(
        requests_ver=requests.__version__,
        this_ver=__version__
    )
    headers = {'user-agent': user_agent, 'Client-ID': client_id}

    response = requests.get(url, timeout=60, headers=headers)
    return response


def get_all_pages(url):
    response = send_request(url)
    yield response
    data = response.json()
    while len(data.get("streams", [])) > 0:
        next_url = data["_links"]["next"]
        response = send_request(next_url)
        yield response
        data = response.json()


def get_image(data):
    height = data['video_height']
    image_url = data['preview']['template']
    image_url = image_url.replace('{width}', '0').replace('{height}', str(height))
    return image_url


def get_image_by_channel(channel_name):
    url = "https://api.twitch.tv/kraken/streams/wraxu?api_version=3"
    response = send_request(url)
    data = response.json()
    image_url = get_image(data)
    return image_url


def get_images_by_game(game_name):
    url = "https://api.twitch.tv/kraken/streams?game={0}".format(game_name)
    image_urls = []
    for response in get_all_pages(url):
        streams_data = response.json()["streams"]
        for stream_data in streams_data:
            image_url = get_image(stream_data)
            if not image_url:
                continue
            image_urls.append(image_url)

    return list(set(image_urls))


def download_images_by_game(game_name):
    image_urls = get_images_by_game(game_name)

    pbar = ProgressBar()
    for image_url in pbar(image_urls):
        image_path = convert_url_to_file_path(image_url)
        download_image(image_url, image_path)


def collect_images_periodically(game_name, wait_time_between_samples=600):
    while True:
        print("{0} - Collection data for {1}".format(str(datetime.datetime.now()), game_name))
        download_images_by_game(game_name)
        time.sleep(wait_time_between_samples)

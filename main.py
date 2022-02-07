import requests
from pathlib import Path
from urllib.parse import urlparse
import os.path
from dotenv import load_dotenv
import telegram
import random
import time


def download_picture(filepath, url, params = None):
    response = requests.get(url, params=params)

    response.raise_for_status()
    with open(filepath, "wb") as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number):
    response = requests.get("https://api.spacexdata.com/v3/launches/")
    response.raise_for_status()
    for index, images in enumerate(response.json()[launch_number]["links"]["flickr_images"]):
        download_picture(f"images/spacex_{index}.svg", images)


def keep_original_extension(url):
    parsing_url = urlparse(url)
    split_url = os.path.splitext(parsing_url.path)
    return split_url[1]


def fetch_nasa_picture(params):
    response = requests.get("https://api.nasa.gov/planetary/apod", params=params)
    response.raise_for_status()
    for index, image in enumerate(response.json()):
        download_picture(
            f"images/nasa_{index}{keep_original_extension(image['hdurl'])}", image["hdurl", params]
        )


def fetch_epic_nasa_picture(params):
    response = requests.get("https://api.nasa.gov/EPIC/api/natural/images", params=params)
    response.raise_for_status()
    for index, image in enumerate(response.json()):
        formated_date = f"{image['date'].split(' ')[0].replace('-', '/')}/png/{image['image']}"
        picture_url = f"https://api.nasa.gov/EPIC/archive/natural/{formated_date}.png"
        download_picture(f"images/epic_nasa{index}{keep_original_extension(picture_url)}", picture_url, params)


if __name__ == "__main__":
    Path("images").mkdir(parents=True, exist_ok=True)
    load_dotenv()

    telegram_bot = telegram.Bot(token=f'{os.getenv("TOKEN_TELEGRAM")}')
    api_nasa_token = os.getenv("API_NASA")
    nasa_params = {"api_key": f"{api_nasa_token}", "count": "5"}
    nasa_epic_params = {"api_key": f"{api_nasa_token}"}
    spacex_launch_number = os.getenv("LAUNCH_NUMBER")
    telegram_chat_id = os.getenv("CHAT_ID")
    sleep_code_time = int(os.getenv("TIME_CODE"))

    fetch_spacex_launch(spacex_launch_number)
    fetch_nasa_picture(nasa_params)
    fetch_epic_nasa_picture(nasa_epic_params)
    while True:
        with open(f"images/{random.choice(os.listdir('images'))}", "rb") as file:
            telegram_bot.send_document(chat_id=telegram_chat_id, document=file)
        time.sleep(sleep_code_time)

import requests
from pathlib import Path
from urllib.parse import urlparse
import os.path
from dotenv import load_dotenv
import telegram
import random
import time


def download_picture(filename, url):
    filename = f"images/{filename}"
    response = requests.get(url)

    response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(response.content)


def fetch_spacex_launch(launch_number):
    response = requests.get("https://api.spacexdata.com/v3/launches/")
    response.raise_for_status()
    for index, images in enumerate(response.json()[launch_number]["links"]["flickr_images"]):
        download_picture(f"spacex_{index}.svg", images)


def keep_original_extension(url):
    parsing_url = urlparse(url)
    split_url = os.path.splitext(parsing_url.path)
    return split_url[1]


def fetch_nasa_picture(params):
    response = requests.get("https://api.nasa.gov/planetary/apod", params=params)
    response.raise_for_status()
    for index, image in enumerate(response.json()):
        download_picture(
            f"nasa_{index}{keep_original_extension(image['hdurl'])}", image["hdurl"]
        )


def fetch_epic_nasa_picture(params):
    response = requests.get("https://api.nasa.gov/EPIC/api/natural/images", params=params)
    response.raise_for_status()
    print(response.json())
    for index, image in enumerate(response.json()):
        formated_date = f"{image['date'].split(' ')[0].replace('-', '/')}/png/{image['image']}"
        response_image = requests.get(
            f"https://api.nasa.gov/EPIC/archive/natural/{formated_date}.png",
            params=params
        )
        with open(f"images/epic_nasa{index}{keep_original_extension(response_image.url)}", "wb") as file:
            file.write(response_image.content)


if __name__ == "__main__":
    Path("images").mkdir(parents=True, exist_ok=True)
    load_dotenv()

    telegram_bot = telegram.Bot(token=f'{os.getenv("TOKEN_TELEGRAM")}')
    updates = telegram_bot.get_updates()
    api_nasa_token = os.getenv("API_NASA")
    api_nasa = {"api_key": f"{api_nasa_token}", "count": "5"}
    api_nasa_epic = {"api_key": f"{api_nasa_token}"}


    fetch_spacex_launch(os.getenv("LAUNCH_NUMBER"))
    fetch_nasa_picture(api_nasa)
    fetch_epic_nasa_picture(api_nasa_epic)
    while True:
        with open(f"images/{random.choice(os.listdir('images'))}", "rb") as file:
            telegram_bot.send_document(chat_id=f'{os.getenv("CHAT_ID")}', document=file)
        time.sleep(int(os.getenv("TIME_CODE")))

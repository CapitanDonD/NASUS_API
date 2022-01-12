import requests
from pathlib import Path
from urllib.parse import urlparse
import os.path
from dotenv import load_dotenv
from pprint import pprint


def install_pictures(filename, url):
    filename = f"images/{filename}"
    response = requests.get(url)

    response.raise_for_status()
    Path("images").mkdir(parents=True, exist_ok=True)
    with open(filename, "wb") as file:
        file.write(response.content)


def fetch_spacex_last_launch():
    response = requests.get("https://api.spacexdata.com/v3/launches/")
    response.raise_for_status()
    for index, images in enumerate(response.json()[74]["links"]["flickr_images"]):
        install_pictures(f"spacex_{index}.svg", images)


def keeping_original_extension(url):
    parsing_url = urlparse(url)
    split_url = os.path.splitext(parsing_url.path)
    return split_url[1]


def install_pictures_nasa(api_key):
    response = requests.get("https://api.nasa.gov/planetary/apod", params=api_key)
    response.raise_for_status()
    for index, image in enumerate(response.json()):
        install_pictures(
            f"nasa_{index}{keeping_original_extension(image['hdurl'])}", image["hdurl"]
        )


def install_pictures_epic_nasa(api_key):
    response = requests.get("https://api.nasa.gov/EPIC/api/natural/images", params=api_key)
    response.raise_for_status()
    for index, image in enumerate(response.json()):
        response_image = requests.get(
            f"https://api.nasa.gov/EPIC/archive/natural/{(image['date'].split(' ')[0].replace('-','/'))}/png/{image['image']}.png",
            params=api_key
        )
        Path("images").mkdir(parents=True, exist_ok=True)
        with open(f"epic_nasa{index}{keeping_original_extension(response_image.url)}", "wb") as file:
            file.write(response_image.content)


load_dotenv()

api_nasa_token = os.getenv("API_NASA")
api_nasa = {"api_key": f"{api_nasa_token}", "count": "4"}
api_nasa_epic = {"api_key": f"{api_nasa_token}"}

print(install_pictures_epic_nasa(api_nasa_epic))
#print(keeping_original_extension("https://apod.nasa.gov/apod/image/2107/LRVBPIX3M82Crop1024.jpg?hahah"))
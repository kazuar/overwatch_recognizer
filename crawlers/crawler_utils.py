
import requests

def download_image(image_url, image_path):
    with open(image_path, "wb") as output_file:
        content = requests.get(image_url).content
        output_file.write(content)
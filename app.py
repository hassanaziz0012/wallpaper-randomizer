import requests
import random
import ctypes
import os
import time
from tqdm import tqdm


CLIENT_ID = "CLIENT_ID" # Get this from creating a Developer account on Unsplash. Replace this with your own CLIENT_ID.

page = random.randint(1, 368)
url = f"https://api.unsplash.com/topics/wallpapers/photos?client_id={CLIENT_ID}&orientation=landscape&page={page}"

response = requests.request("GET", url)

result = response.json()
image = random.choice(result)

image_url = image["urls"]["raw"]

print(f'Downloading image from Unsplash: {image_url}')

response = requests.request("GET", image_url, stream=True)

total_image_size = int(response.headers.get('content-length', 0))
block_size = 1024
progress_bar = tqdm(total=total_image_size, unit='iB', unit_scale=True)

with open('image.png', 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)

path = os.path.abspath('image.png')

progress_bar.close()
if total_image_size != 0 and progress_bar.n != total_image_size:
    print('Error: Something went wrong.')

print('Downloaded Image. Changing wallpaper.')

print(path)
ctypes.windll.user32.SystemParametersInfoW(20, 0, str(path) , 0)

print("Finished changing wallpaper. Exiting...")
time.sleep(.5)

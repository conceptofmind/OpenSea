
# 11/28/2021
# Made by DanChan
# NFT Stealer (OpenSea)

import requests
import os
import json
import math

CollectionName = "Collection Name".lower()

# Get information regarding collection

collection = requests.get(f"http://api.opensea.io/api/v1/collection/{CollectionName}?format=json")

if collection.status_code == 404:
    print("NFT Collection not found.\n\n(Hint: Try changing the name of the collection in the Python script, line 11.)")
    exit()

collectioninfo = json.loads(collection.content.decode())

# Create image folder if it doesn't exist.

if not os.path.exists('./images'):
    os.mkdir('./images')

if not os.path.exists(f'./images/{CollectionName}'):
    os.mkdir(f'./images/{CollectionName}')

# Get total NFT count

count = float(collectioninfo["collection"]["stats"]["count"])

# Opensea limits to 50 assets per API request, so here we do the division and round up.

iter = math.ceil(count / 50)

# Iterate through numbers 0000 - 9999
for i in range(iter):
    offset = i * 50
    data = json.loads(requests.get(f"https://api.opensea.io/api/v1/assets?order_direction=asc&offset={offset}&limit=50&collection={CollectionName}&format=json").content.decode())

    for asset in data["assets"]:
      formatted_number = f"{int(asset['token_id']):04d}"

      # Check if image already exists, if it does, skip it
      if os.path.exists(f'./images/{CollectionName}/{formatted_number}.png'):
          print(f"{CollectionName} #{formatted_number} already downloaded, skipping")

      else:
          # Make the request to the URL to get the image
          if not asset["image_original_url"] == None:
            image = requests.get(asset["image_original_url"])
          else:
            image = requests.get(asset["image_url"])

          # If the URL returns status code "200 Successful", save the image into the "images" folder.
          if image.status_code == 200:
              file = open(f"./images/{CollectionName}/{formatted_number}.png", "wb+")
              file.write(image.content)
              file.close()
              print(f"{CollectionName} #{formatted_number} successfully downloaded!")
          
          # If the URL returns a status code other than "200 Successful", alert the user and don't save the image
          else:
              print(f"{CollectionName} #{formatted_number} returned HTTP Status {image.status_code}, skipping")
              print(image.content.decode())

print(f"\n\n\nFinished downloading collection. You can find the images in the images/{CollectionName} folder.")
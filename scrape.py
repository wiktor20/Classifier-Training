import os, requests, lxml, re, json, urllib.request
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"
}

params = {
    "q": "FedEx", # search query
    "tbm": "isch",                # image results
    "hl": "en",                   # language of the search
    "gl": "us",                   # country where search comes from
    "ijn": "0"                    # page number
}

html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
soup = BeautifulSoup(html.text, "lxml")

google_images = []

all_script_tags = soup.select("script")

# # https://regex101.com/r/48UZhY/4
matched_images_data = "".join(re.findall(r"AF_initDataCallback\(([^<]+)\);", str(all_script_tags)))

matched_images_data_fix = json.dumps(matched_images_data)
matched_images_data_json = json.loads(matched_images_data_fix)

# https://regex101.com/r/VPz7f2/1
matched_google_image_data = re.findall(r'\"b-GRID_STATE0\"(.*)sideChannel:\s?{}}', matched_images_data_json)

# https://regex101.com/r/NnRg27/1
matched_google_images_thumbnails = ", ".join(
    re.findall(r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]',
                str(matched_google_image_data))).split(", ")

thumbnails = [
    bytes(bytes(thumbnail, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for thumbnail in matched_google_images_thumbnails
]

# removing previously matched thumbnails for easier full resolution image matches.
removed_matched_google_images_thumbnails = re.sub(
    r'\[\"(https\:\/\/encrypted-tbn0\.gstatic\.com\/images\?.*?)\",\d+,\d+\]', "", str(matched_google_image_data))

# https://regex101.com/r/fXjfb1/4
# https://stackoverflow.com/a/19821774/15164646
matched_google_full_resolution_images = re.findall(r"(?:'|,),\[\"(https:|http.*?)\",\d+,\d+\]", removed_matched_google_images_thumbnails)

full_res_images = [
    bytes(bytes(img, "ascii").decode("unicode-escape"), "ascii").decode("unicode-escape") for img in matched_google_full_resolution_images
]

for img in full_res_images:
    url = img
    data = requests.get(url).content
    path = "Classifier-Training\\data\\"
    f = open(path + 'img' + str(full_res_images.index(url)) + '.jpg','wb')
    f.write(data)
    f.close()
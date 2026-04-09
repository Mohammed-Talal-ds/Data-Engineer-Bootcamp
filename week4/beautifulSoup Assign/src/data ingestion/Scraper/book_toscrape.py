
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import string
import pandas as pd
from pathlib import Path

# config path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
data_path = BASE_DIR / "data"
IMAGE_PATH = BASE_DIR / "images" / "raw_data_images"

URL = 'https://books.toscrape.com/catalogue/'
Books_list = []
page_num = 1
url = URL
headers = {
    "User-Agent": "Mozilla/5.0"
}
while url and page_num <= 20:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_books = soup.findAll('article', class_ = 'product_pod')
    for item in raw_books:
        name = item.find('h3').find('a')['title']
        rating = item.find('p', class_= 'star-rating')['class'][1]
        price = item.find('p', class_= 'price_color').text
        image_src = item.find('img')['src']
        cleaned_name = name.translate(str.maketrans('','',string.punctuation))
        # Downlaod images
        image_url = urljoin(URL,image_src)
        img_content = requests.get(image_url).content
        with open('../../../images/raw_data_images' + cleaned_name.replace(" ", "_")[:30] + '.png', "wb") as file:
            file.write(img_content)
        Books_list.append({
            "name": name,
            "rating": rating,
            "price": price,
            "img_url": image_url,
        })
    nxt_btn = soup.find('li', class_ = 'next')
    print(f'Page{page_num} Done.')
    page_num += 1
    url =f'https://books.toscrape.com/catalogue/page-{page_num}.html' if nxt_btn else None


df = pd.DataFrame(Books_list)
df.to_csv(f'../../../data/raw_data.csv')
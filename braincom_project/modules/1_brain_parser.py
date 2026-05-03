import pprint

import requests
from bs4 import BeautifulSoup
from load_django import *
from parser_app.models import BrainProduct

headers = {
    'User-Agent': 'Mozilla/5.0'
}

url = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html"

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

product = {}
specs = {}
images = []

def clean_text(text):
    return " ".join(text.replace("\xa0", " ").split())

try:
    product['title'] = soup.find('h1', class_='desktop-only-title').get_text(strip=True)
except:
    product['title'] = None

try:
    block = soup.find("div", id="br-characteristics")
    inner = block.find("div", class_="br-wrap-block br-elem-block")
    for item in inner.find_all("div", class_="br-pr-chr-item"):
        for row in item.select("div > div"):
            spans = row.find_all("span")
            if len(spans) == 2:
                key = clean_text(spans[0].get_text())
                value = clean_text(spans[1].get_text(" "))

                if key in specs:
                    if isinstance(specs[key], list):
                        specs[key].append(value)
                    else:
                        specs[key] = [specs[key], value]
                else:
                    specs[key] = value

    product['specs'] = specs
except:
    product['characteristics'] = None

# get() method returns None by default if the key is not found
product['manufacturer'] = specs.get("Виробник")
product['color'] = specs.get("Колір")
product['memory'] = specs.get("Вбудована пам'ять")
product['screen_diagonal'] = specs.get("Діагональ екрану")
product['screen_resolution'] = specs.get("Роздільна здатність екрану")
try:
    product['product_code'] = soup.select_one(".br-pr-code-val").get_text(strip=True)
except:
    product['product_code'] = None
try:
    text = soup.select_one(".brackets-reviews").get_text(strip=True)
    product['reviews_count'] = int(''.join(c for c in text if c.isdigit()))
except:
    product['reviews_count'] = None
try:
    product['price_regular'] = soup.select_one(".br-pr-no-del strong").get_text(strip=True)
except:
    product['price_regular'] = None

try:
    product['price_sale'] = soup.select_one(".br-pr-no-del strong").get_text(strip=True)
except:
    product['price_sale'] = None

try:
    for img in soup.select(".br-main-img"):
        src = img.get("src")
        if src:
            images.append(src)
    product['images'] = images
except:
    product['images'] = None

BrainProduct.objects.update_or_create(
    product_code=product.get("product_code"),
    defaults={
        "title": product.get("title"),
        "manufacturer": product.get("manufacturer"),
        "color": product.get("color"),
        "memory": product.get("memory"),
        "price_regular": product.get("price_regular"),
        "price_sale": product.get("price_sale"),
        "images": images,
        "reviews_count": product.get("reviews_count"),
        "screen_diagonal": product.get("screen_diagonal"),
        "screen_resolution": product.get("screen_resolution"),
        "characteristics": specs,
    },
)
pprint.pprint(product)




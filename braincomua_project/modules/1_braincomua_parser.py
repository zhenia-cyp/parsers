from pprint import pprint

from playwright.sync_api import sync_playwright
import re

from load_django import *
from parser_app.models import BrainComUaProduct


PRODUCT_URL = "https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_15_128GB_Black-p1044347.html"
product = {}


def clean_text(text):
    return " ".join(text.replace("\xa0", " ").split())


def first_int(text):
    text = text or ""
    digits = "".join(char for char in text if char.isdigit())
    return int(digits) if digits else None


def save_product(product):
    BrainComUaProduct.objects.update_or_create(
        product_code=product.get("product_code"),
        defaults={
            "title": product.get("title"),
            "manufacturer": product.get("manufacturer"),
            "color": product.get("color"),
            "memory": product.get("memory"),
            "price_regular": product.get("price_regular"),
            "price_sale": product.get("price_sale"),
            "images": product.get("images", []),
            "reviews_count": product.get("reviews_count"),
            "screen_diagonal": product.get("screen_diagonal"),
            "screen_resolution": product.get("screen_resolution"),
            "characteristics": product.get("characteristics", {}),
        },
    )



def parse():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
        args=["--start-maximized"]
        )
        page = browser.new_page(no_viewport=True)

        page.goto(PRODUCT_URL, wait_until="domcontentloaded")
        page.wait_for_load_state("domcontentloaded")

        try:
            title = page.locator("//h1[contains(@class, 'desktop-only-title')]")
            title.wait_for(state="visible", timeout=15000)
            product["title"] = clean_text(title.inner_text())
            product_id = title.get_attribute("data-pid")
        except:
            product["title"] = None
            product_id = None

        try:
            price_block = page.locator(
                f"//div[contains(@class, 'br-pr-price') and .//div[@data-pid='{product_id}']]"
            )
            price_text = clean_text(price_block.first.inner_text())
            prices = re.findall(r"\d[\d\s]*", price_text)
            prices = [clean_text(price) for price in prices]

            product["price_regular"] = prices[-1] if prices else None
            product["price_sale"] = prices[0] if len(prices) > 1 else None
        except:
            product["price_regular"] = None
            product["price_sale"] = None

        try:
            product_code = page.locator("//span[contains(@class, 'br-pr-code-val')]")
            product["product_code"] = product_code.first.inner_text().strip()
        except:
            product["product_code"] = None

        try:
            image_urls = []
            images = page.locator(f"//img[contains(@src, '{product['product_code']}')]")

            for index in range(images.count()):
                src = images.nth(index).get_attribute("src")

                if src and "small" not in src and src not in image_urls:
                    image_urls.append(src)

            product["images"] = image_urls
        except:
            product["images"] = []

        try:
            reviews_text = page.locator("a.brackets-reviews:visible").first.inner_text()
            product["reviews_count"] = first_int(reviews_text)
        except:
            product["reviews_count"] = None

        try:
            characteristics = {}
            rows = page.locator("//div[@id='br-characteristics']//div[contains(@class, 'br-pr-chr-item')]//div[span]")

            for index in range(rows.count()):
                spans = rows.nth(index).locator(":scope > span")

                if spans.count() != 2:
                    continue

                key = clean_text(spans.nth(0).inner_text())
                value = clean_text(spans.nth(1).inner_text())

                if not key or not value:
                    continue

                if key in characteristics:
                    if isinstance(characteristics[key], list):
                        characteristics[key].append(value)
                    else:
                        characteristics[key] = [characteristics[key], value]
                else:
                    characteristics[key] = value

            product["characteristics"] = characteristics
        except:
            product["characteristics"] = {}

        product["manufacturer"] = product["characteristics"].get("Виробник")
        product["color"] = product["characteristics"].get("Колір")
        product["memory"] = product["characteristics"].get("Вбудована пам'ять")
        product["screen_diagonal"] = product["characteristics"].get("Діагональ екрану")
        product["screen_resolution"] = product["characteristics"].get("Роздільна здатність екрану")
        pprint(product)




if __name__ == "__main__":
    parse()
    save_product(product)
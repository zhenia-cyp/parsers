from load_django import *
from parser_app.models import BrainProduct


obj, created = BrainProduct.objects.update_or_create(
    product_code="test-001",
    defaults={
        "title": "Test product from modules",
        "manufacturer": "Test manufacturer",
        "color": "Black",
        "memory": "256GB",
        "price_regular": "1000",
        "price_sale": "900",
        "images": ["https://example.com/image.jpg"],
        "reviews_count": 5,
        "screen_diagonal": "6.9",
        "screen_resolution": "2868x1320",
        "characteristics": {"test": "ok"},
    },
)

print(f"Saved product id={obj.title}, created={created}")

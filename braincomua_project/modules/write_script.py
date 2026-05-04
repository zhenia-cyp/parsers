from load_django import *
from parser_app.models import BrainComUaProduct


BrainComUaProduct.objects.update_or_create(
    product_code="test-nokia-001",
    defaults={
        "title": "Test Nokia",
        "manufacturer": "Test Finland",
        "color": "red",
        "memory": "256GB",
        "price_regular": "7000",
        "price_sale": "5000",
        "images": ["https://example.com/image.jpg"],
        "reviews_count": 15,
        "screen_diagonal": "6.9",
        "screen_resolution": "2868x1320",
        "characteristics": {"test": "ok"},
    },
)

from load_django import *
from parser_app.models import BrainComUaProduct


for product in BrainComUaProduct.objects.all().order_by("id"):
    print(
        product.title,
        product.manufacturer
    )

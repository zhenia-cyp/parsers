from load_django import *
from parser_app.models import BrainProduct


for product in BrainProduct.objects.all().order_by("id"):
    print(
        product.title
    )

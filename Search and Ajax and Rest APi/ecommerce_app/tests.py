from django.test import TestCase
from .models import Product

# Create your tests here.

class Test(TestCase):
    def test_product(self):
        vi = Product.objects.create(product_name="Test",price=10,old_price=23)
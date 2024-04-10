from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import admin


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, null=True,on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=50)
    mrp = models.FloatField()
    price = models.FloatField()
    tax_percentage = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="images")

    MONTH_CHOICES = (
        ("JANUARY", "January"),
        ("FEBRUARY", "February"),
        ("MARCH", "March"),
        # ....
        ("DECEMBER", "December"),
    )

    month = models.CharField(max_length=9,
                    choices=MONTH_CHOICES,
                    default="JANUARY")
    
    @admin.display(
    boolean=True,
    ordering="mrp",
     description="Product Price"   
    )
    def price(self):
        return True

class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books_written')
    editor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books_edited')
    published_date = models.DateField(null = True, blank = True)

    def was_published_recently(self):
        return False
        # from django.utils import timezone
        # import datetime
        # now = timezone.now()
        # return now - datetime.timedelta(days=1) <= self.published_date <= now

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article2(models.Model):
    title = models.CharField(max_length=100)
    tags = models.ManyToManyField(Tag, related_name='articles')

class StockEntry(models.Model):
    posting_date = models.DateTimeField(auto_now_add=True)
    warehosue = models.CharField(max_length=50)
    stock_type = models.CharField(max_length=50,choices=[
        ("Material Receipt","Material Receipt")
    ])

class StockEntryItems(models.Model):
    product = models.ForeignKey(StockEntry,on_delete=models.SET_NULL,null=True)
    stock_qty = models.FloatField()
    price = models.DecimalField(max_digits=4,decimal_places=3)



def validate_test(value):
    if not value:
        raise ValidationError("The fiels can't be empty.")
    else:
        return value

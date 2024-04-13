from typing import Collection
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.files.storage import FileSystemStorage
import os


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
    def was_published_recently(self):
        return "s"

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

class Discount(models.Model):
    d_percentage = models.DecimalField(max_digits=3,decimal_places=2,default = 50.0)
    class Meta:
        db_table = "product_discount"

class DiscountInfo(models.Model):
    d_percentage = models.DecimalField(max_digits=3,decimal_places=2,default = 50.0,db_column='product_d_percentage')
    class Meta:
        db_table = "product_discounts"
        db_table_comment = "it is used to specify product discounts."

def get_choices():
    # return {1:"one",None:"Please Dynamic Choice."}
    return [("db","label"),(None,"Select Choice"),("db","hey db")]

def json_fun():
    import json
    return json.dumps({"s","s"})

class FieldTypesCheckL(models.Model):
    @staticmethod
    def get_choicess():
        return [
                    (
                        "Audio",
                        (
                            ("vinyl", "Vinyl"),
                            ("cd", "CD"),
                        ),
                    ),
                    (
                        "Video",
                        (
                            ("vhs", "VHS Tape"),
                            ("dvd", "DVD"),
                        ),
                    ),
                    ("unknown", "Unknown"),
                ]
    
    class AllChoices(models.TextChoices):
        ch1 = ("iphone",_("Iphone"))
    
    class Bike(models.TextChoices):
        Bajaj = "bj"
        Honda = 'hd'
    
    class Suit(models.IntegerChoices):
        DIAMOND = 1
        SPADE = 2
        HEART = 3
        CLUB = 4
        __empty__ = _("Please Choose Choice.")

    suit = models.IntegerField(choices=Suit,error_messages={"required":"This Field can't be empty."},help_text="Please choose")

    class MoonLandings(datetime.date, models.Choices):
        APOLLO_11 = 1969, 7, 20, "Apollo 11 (Eagle)"
        APOLLO_12 = 1969, 11, 19, "Apollo 12 (Intrepid)"
        APOLLO_14 = 1971, 2, 5, "Apollo 14 (Antares)"
        APOLLO_15 = 1971, 7, 30, "Apollo 15 (Falcon)"
        APOLLO_16 = 1972, 4, 21, "Apollo 16 (Orion)"
        APOLLO_17 = 1972, 12, 11, "Apollo 17 (Challenger)"

    title = models.CharField(max_length=100)
    bike_name = models.CharField(max_length = 100,blank = True,unique=True,null = True)
    model = models.CharField(max_length=100,choices=[(None,"Please Select Choice.."),("FZS","fzs"),
                                                    ("FZX","fzx")],default = "FZS")
    year = models.CharField(max_length=100,choices=[(None,"Please Select Choice.."),("2012","2k12"),
                                                    ("2k13","2k13")],default = "FZS",null=True,blank=True)
    dynamic_choices = models.CharField(max_length=100,choices = get_choices())
    choices = models.CharField(max_length=100,choices = get_choicess())
    cls_choices = models.CharField(max_length=100,choices = AllChoices)
    enum_choices = models.CharField(max_length=100,choices = Bike)
    # moon_landing = models.CharField(max_length=100,choices = MoonLandings)

    dd_default = models.CharField(max_length=10,db_default = "i am de default",blank=True)
    dd_index = models.CharField(max_length=10,db_index = True,blank=True)


    # json_ob = models.JSONField(editable=False,default = json_fun())

    checking = models.CharField(max_length=100,blank=True,null=False)

    checking_2 = models.CharField(max_length=100,blank=True,null=False)

    def __str__(self):
        return self.title


def validate_1(obj):
    # raise ValidationError("Date should be Today..!")
    pass

def validate_2(obj):
    # raise ValidationError("Date should be different..!")
    pass

def get_path(obj,filename):
    print("--------------filename",filename)
    return filename

file_storage = FileSystemStorage(location="/system_storage")

def get_file_path():
    from django.conf import settings
    print("----------------------",settings.MEDIA_ROOT)
    return os.path.join(settings.MEDIA_ROOT,"images")


class FieldTypesCheckL2(models.Model):
    file_stor = models.FileField(upload_to=file_storage)
    file_path = models.FilePathField(path=get_file_path,recursive=True,allow_files = True,allow_folders=True)
    # @staticmethod
    # def validate_1(obj):
    #     if not obj.pub_date == datetime.datetime.today():
    #         raise ValidationError("Date should be Today..!")
    
    # @staticmethod
    # def validate_2(obj):
    #     if obj.pub_date == datetime.datetime.today():
    #         raise ValidationError({"pub_date":"Date should be different..!"})

    pub_date = models.DateField()
    title = models.OneToOneField(FieldTypesCheckL,verbose_name=_("One Army"), on_delete=models.CASCADE,related_name = "one_to_one",unique_for_date="pub_date")
    many = models.ManyToManyField(FieldTypesCheckL)
    valida = models.ForeignKey(FieldTypesCheckL,validators=[validate_1,validate_2],null=True,on_delete=models.SET_NULL,related_name = "validate_field")

    date_now = models.DateField(auto_now=True)
    datetime_now = models.DateTimeField(auto_now=True)
    datetime_cr = models.DateTimeField(auto_now_add=True)


    duration_f = models.DurationField(null = True)
    email_f = models.EmailField(null = True)
    file_f = models.FileField(upload_to="files")
    file_d = models.FileField(upload_to="files/%Y/%m/%d/")
    file_fun = models.FileField(upload_to=get_path)

    # def clean(self):
    #     self.title = "Gopis"
    #     self.bike_name = "Yamahass"
    #     raise ValidationError("kk")
    # def full_clean(self):
    #     pass


def validate_test(value):
    if not value:
        raise ValidationError("The fiels can't be empty.")
    else:
        return value

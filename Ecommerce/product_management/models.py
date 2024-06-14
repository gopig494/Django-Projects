from typing import Collection
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
import datetime
from django.core.files.storage import FileSystemStorage
import os
import uuid
from django.conf import settings


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
    # return json.dumps({"s","s"})
    return {"model":"json"}

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

    dd_default = models.CharField(max_length=100,db_default = "i am",blank=True)
    dd_index = models.CharField(max_length=100,db_index = True,blank=True)


    # json_ob = models.JSONField(editable=False,default = json_fun(),null=True)

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
    fip_ad = models.GenericIPAddressField(verbose_name="FIP Address",null=True)
    file_stor = models.FileField(upload_to=file_storage)
    file_path = models.FilePathField(path=get_file_path,recursive=True,allow_files = True,allow_folders=True)
    gen_field = models.GeneratedField(expression = F("file_path"),output_field = models.FilePathField(),db_persist = True)
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

    img_h = models.IntegerField()
    img_w = models.IntegerField()
    img_f = models.ImageField(max_length=100,upload_to="images/",height_field="img_h",width_field="img_w")

    # json_ob = models.JSONField(default = {},null=True)

    chr = models.CharField(max_length=200)
    
    slug_f = models.SlugField(max_length=100)

    # def clean(self):
    #     self.title = "Gopis"
    #     self.bike_name = "Yamahass"
    #     raise ValidationError("kk")
    # def full_clean(self):
    #     pass

class FieldCheck3(models.Model):
    title = models.CharField(max_length=100)
    URL = models.SlugField(max_length=100,unique=True)
    url_fiel = models.URLField(max_length=100)

    def description(self):
        pass

class CheckUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Person(models.Model):
    title = models.CharField(max_length=100)
    groups = models.ManyToManyField('Group', symmetrical=True)
    group_1 = models.ManyToManyField('Group',symmetrical=False,related_name="group_1")

class Group(models.Model):
    title = models.CharField(max_length=100)
    members = models.ManyToManyField('Person', symmetrical=True, null = True, blank = True)
    uuids = models.ManyToManyField(CheckUUID, null = True, blank = True)
    group = models.ManyToManyField("self", null = True, blank = True)

class User(models.Model):
    username = models.CharField(max_length=50)
    following = models.ManyToManyField('self', related_name='followers',blank=True)

class User_1(models.Model):
    username = models.CharField(max_length=50)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers',blank=True)



class Product_Forign(models.Model):
    title = models.CharField(max_length=100)
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)


    class Meta:
        abstract = True

def set_def():
    return 1

# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     # Add custom fields or methods if needed
#     pass

# class UserProfile(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ForignOpts(models.Model):
    product_forign = models.ForeignKey(CheckUUID,on_delete = models.PROTECT)
    filed_c3 = models.ForeignKey(FieldCheck3,on_delete = models.RESTRICT,to_field='URL')
    filed_c2 = models.ForeignKey(FieldTypesCheckL2,on_delete = models.SET_NULL,null=True)
    filed_l = models.ForeignKey(FieldTypesCheckL,on_delete = models.SET_DEFAULT,default=1)
    dis = models.ForeignKey(Discount,on_delete = models.SET_DEFAULT,default=1)
    dis_info = models.ForeignKey(DiscountInfo,on_delete = models.SET(set_def))
    se_itm = models.ForeignKey(StockEntry,on_delete = models.DO_NOTHING)
    b = models.ForeignKey(Book,on_delete = models.DO_NOTHING,limit_choices_to = {"author":1},related_name='+')


def validate_test(value):
    if not value:
        raise ValidationError("The fiels can't be empty.")
    else:
        return value


class Person_1(models.Model):
    name = models.CharField(max_length=100)

class Parent(models.Model):
    parent_field_me = models.CharField(max_length=100)


class Child(Parent):
    child_field = models.CharField(max_length=100)
    parent_link = models.OneToOneField(Parent, on_delete=models.CASCADE, parent_link=True,related_name="child_1",related_query_name="child_1_query")


# while creating many to many field djngo will create the new table to store many to many fileld values

# we can override this by using 'throgh' argument.

class Group_1(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Person_1, through='Membership_1',through_fields=("group", "person"))
    parent = models.ManyToManyField(Parent)

class Membership_1(models.Model):
    group = models.ForeignKey(Group_1, on_delete=models.CASCADE)
    person = models.ForeignKey(Person_1, on_delete=models.CASCADE)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=100)

class Parent_2(models.Model):
    parent_field = models.CharField(max_length=100)

class DescriptorClass:
    def __init__(self, field_type):
        print("-----field_type",field_type)
        self.field_type = field_type
        self._value = None

    def __get__(self, instance, owner):
        print("Getting value...")
        return self._value

    def __set__(self, instance, value):
        print("Setting value...")
        if not isinstance(value, self.field_type):
            raise ValueError(f"Expected {self.field_type.__name__}, got {type(value).__name__}")
        self._value = value


class Child2(Parent_2):
    child_fields_1 = models.CharField(max_length=100)
    parent_links_1 = models.OneToOneField(Parent, on_delete=models.CASCADE,related_name = "child2",related_query_name="child_2_query")
    descrip = DescriptorClass(field_type = models.CharField(max_length=100))

name_field_type = Child2._meta.get_field('child_fields_1').get_internal_type()
from django.db import connections
connection = connections['default']
name_field_type_2 = Child2._meta.get_field('child_fields_1').db_type(connection= connection)
name_field_type_3 = Child2._meta.get_field('child_fields_1').rel_db_type(connection= connection)
name_field_type_4 = Child2._meta.get_field('id').auto_created
print("-----------------name_field_type----------------",name_field_type)
print("-----------------name_field_type_2----------------",name_field_type_2)
print("-----------------name_field_type_3----------------",name_field_type_3)
print("-----------------name_field_type_4----------------",name_field_type_4)


class Car(models.Model):
    title = models.CharField(max_length=100,null = True, blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    model_nos = models.CharField(max_length=100,unique=True)

    def clean_fields(self, exclude=None):
        print("-----------------clean_fields----------------")
        super().clean_fields(exclude=exclude)
        # Custom validation logic
        if self.price and self.price < 0:
            raise ValidationError({"price":"price cannot be negative."})
    
    def clean(self):
        print("-----------------clean----------------")
        # Call the super clean method to ensure any parent class clean() methods are called.
        super().clean()
        if not self.title:
            raise ValidationError({"title":"title needed"})

    def validate_unique(self,exclude=None):
        print("-----------------validate unique----------------")
        # Call the super clean method to ensure any parent class clean() methods are called.
        super().validate_unique()
        if not self.title:
            raise ValidationError({"title":"title needed"})
    
    def validate_constraints(self,exclude=None):
        print("-----------------validate unique----------------")
        # Call the super clean method to ensure any parent class clean() methods are called.
        super().validate_constraints()
        if not self.title:
            raise ValidationError({"title":"title needed"})
    

    def full_clean(self,exclude=None, validate_unique=True, validate_constraints=True):
        super().full_clean(exclude=None, validate_unique=True, validate_constraints=True)


    @classmethod
    def create(cls,**kwargs):
        print("-----------------create----------------",kwargs)
        book = cls(title = kwargs.get("title"))
        return book
    
    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        print("-----------------------------------cls method callings--------------------------------")
        return instance

    def save(self, *args, **kwargs):
        print("-----------------save----------------calling",)
        super().save(*args, **kwargs)

    def refresh_from_db(self, using=None, fields=None, **kwargs):
        print("-----------------refresh_from_db----------------calling",)
        super().refresh_from_db(using, fields, **kwargs)

    
    
# book_1 = Car.create(title = "book 1")
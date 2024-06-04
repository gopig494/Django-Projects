from typing import Collection
from django.db import models
from datetime import date
from django.db.models import F,Q
from django.db.models import DEFERRED
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS

# Create your models here.

from datetime import date

from django.db import models


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200,unique=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)
    modified = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.headline
    
    class Meta:
        ordering = ["headline"]
        verbose_name = "Entry Verbosue"
  
class Production(models.Model):
    name = models.CharField(max_length=100)
    values = models.JSONField(null=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,related_name="entry_forign")
    entries = models.ManyToManyField(Entry)

# Review models

class Location(models.Model):
    city = models.CharField(verbose_name="Current City",max_length=20)

    # forign key is many to one field

    blog = models.ForeignKey(Blog,verbose_name="Blog",on_delete=models.CASCADE)

    # we can create self relationship

    # first way

    parent_location = models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,default=None)

    def __str__(self):
        return self.city


# we can import and use another app models here like forignkey and many to many field

# This sort of reference, called a lazy relationship, can be useful when resolving circular import dependencies between two applications.

from product_management.models import Category

class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Category Name", on_delete=models.CASCADE)

    # in this case when we tring to delete the category attached to this model

    # the model record also will be deleted depending upon casecade nature

    # so the pre_delete and post_delete signales will be triggered and delete not triggered

    # if we set like below we can't use backward relationship fron category model 

    # like category__category 

    category = models.ForeignKey(Category, verbose_name="Category Name", on_delete=models.CASCADE,related_name="+")
    Level_Choices = models.TextChoices("Level_Choices","1 2 3 4")
    level = models.CharField(max_length=100,choices=Level_Choices)

    class Meta:
        ordering = ["-level"]

    def __str__(self):
        return self.level

# learn about meta in models

# use absraction 

# we can use the model anyware in the project with the fieldnames

# now the example use the same file to explore

class AbstractCar(models.Model):
    car_model = models.CharField(max_length=100)

    class Meta:
        abstract = True

# here the car model having both car_model field and colour field

# just reusability takes place 

class Car(AbstractCar):
    colour = models.CharField(max_length=40)

class CustomManager(models.Manager):
    def get_data(self):
        print("-------self.all",self.all())
        return self.all()

    # def create(self,**kwargs):
    #     raise IndexError

    # If you want to modify the initial QuerySet returned by the manager, you can override the get_queryset method:
    # def get_queryset(self) -> models.QuerySet:
    #     return super().get_queryset().filter(name__contains="g")
    
class LearnQSet(models.QuerySet):
    def get_all(self):
        return self.filter(name__contains="g")

class LearnMeta(models.Model):
    name = models.CharField(max_length = 30)
    age = models.IntegerField()
    info = models.CharField(max_length=30,blank=True)
    product = models.ManyToManyField(Product)
    product_forign = models.ForeignKey(Product,on_delete=models.CASCADE,related_name = "porducts")



    # override the objects manager

    # we can create multiple manager and make attribute like below then start to use them

    # objects = CustomManager()

    # custom manager class

    # if we defind any custom managers the default manager `object` manager will the deleted or none 
    custom_manager = CustomManager()

    # if you want to use object manager as well as custom managers , we must specifi the objects manager also
    objects = CustomManager()

    # different method to create manager

    qset_manager = LearnQSet.as_manager()


    def __str__(self):
        # return f'{self.name}  -  {self.age}'
        return self.name

    class Meta:
        # the table will be created under customer app like customer_learnmeta
        # app_label = "customer"
        # by default the `object` manager is used we can change the name by using below attr
        base_manager_name = "custom_manager"

        # we can change the table name 
        # in general the table name in database will be appname_classname
        # to override this below ins
        # internally the database name will be chnaged but when using ORM you have to use the model class name.
        db_table = "meta_learning"

        # documentation or instruction about our models we can use db_table command

        db_table_comment = "User to learn meta in django"

        # table space we can use different database to store and create the data for indexing purpose

        # options = {'tablespace': 'my_tablespace'}

        # from django.db import connection

        # with connection.cursor() as cursor:
        #     cursor.execute("CREATE TABLE my_table (...) TABLESPACE my_tablespace")

        # default manager

        # by default the objects manger is used to fetch the data and we can create alternative managers like above

        # if no manager specified the default manager will be used like below

        # Override default_manager_name to use custom_manager as the default manager

        default_manager_name = "custom_manager"

        # default related name
        # by default djnago takes the related model name and _set to fethc the data
        # if many to many field having table name in master table
        # we can use master_table_set from the table name which means many to many field name

        default_related_name = "get_meta"

        # decending order 
        # which used in latest and earlist function call tp return a sigle record 
        # see the view2.py for more info

        get_latest_by = "-age"

        # order by the forign key values by their field names

        # ordering and order_with_resect_to can't be used at same time if we use the order_with_respect_to it throw error

        # you can see the product is forign key then the product table the ordering isby ht efield 'level'

        # so when we use LearnMeta.objects.all() the ordering is overided by the forign key field

        # so the ordering is depending on the forign key field only or ordering overided

        # explicily we can get the order by calling the function from related model

        # it willnot reflected in admin portal it only used when using the objects to fetch the data

        # meta = Product.objects.all()
        # mets.get_learnmeta_order()

        # we can also set the order then fetch the data

        # meta = Product.objects.all()
        # mets.set_learnmeta_order(['learnmeta primary keys'])


        # to get next and previous values in order we can use
        # meta = Product.objects.all()
        # meta.get_next_in_order()
        # meta.get_previous_in_order()

        # order_with_respect_to = "product_forign"

        # ordering

        # depecing upon the list the fethcing order will be decided

        # it will order the records in admin portal also

        # ascening order 

        # ordering = ["age"]

        # decending order

        # ordering = ["-age"]

        # randomly

        # ordering = ["?"]

        # we can throw the null values to last by below wxpression
        
        ordering = [F("name").asc(nulls_last = True)]


        # permissions 

        # below code is the syntax , these are the customized permissions names

        # permissions = [
        #     ("can_view_mymodel", "Can view MyModel"),
        #     ("can_change_mymodel", "Can change MyModel"),
        #     ("can_delete_mymodel", "Can delete MyModel"),
        # ]

        # default permissions

        default_permissions = ["add","change","delete","view"]

# if you want to create a model that only reference of already existing table schema
# in this table django won't do any table modification when make migrations like alter table, create table
# the managed keyword is used to matching model with existing tables schema which means the table is already created
# we are going to only use the table not modifying anyting on it.

# in this table the name,id just like a form only in admin , if i hide the attribute and make migrations there is noting happen

# because it just referering existing schema only

# if we using many to many field like relation fields it eill vary refer in django documentation

class LearnManaged(models.Model):
    name = models.TextField()
    id = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = "testing_managed"

        # ---
        # select_on_save is a model meta option in Django that determines if Django will use the pre-1.6 
        # django.db.models.Model.save() algorithm. The old algorithm uses SELECT to determine if there 
        # is an existing row with the same primary key, and if so, it updates that row instead of inserting a new one.
        select_on_save = True
        # However, it's worth noting that select_on_save is not a recommended approach, as it can lead to 
        # performance issues and is not compatible with all databases. The default behavior of Django's save()
        #  method is to use an INSERT statement, and if a row with the same primary key already exists, 
        # it will raise an IntegrityError.

        # If you need to update an existing row instead of inserting a new one, it's recommended to use the 
        # update_or_create() method or the get_or_create() method, which are more efficient and reliable.
        # ---


# In this example, ProxyModel is a proxy model(MyPerson) based on Person. It doesn't create its own database table; instead, 
# it operates on the same table as LearnManaged. 
# You can add custom methods, override existing ones, or customize behavior without affecting the original model.
# you can't add custom fields in it
# we can override the methods like create,save,delete

class Person(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        # we can mention indexing in meta
        indexes = [
            models.Index(fields=["first_name"]), #index will be created and column name will be auto generated 
            # models.Index(fields=["first_name","last_name"]), #indexing will be created for both fields
            # models.Index(fields=["first_name"],name="first_name_indexing"), #the column name will the name args value
            # models.Index(fields=["first_name","last_name"],name="first_name_last_name_indexing"), #indexing will be created for both fields
        ]

        # in databaee the first name and last_name should be unique

        # it won't work for manytomany fields
        # we can  use list of list
        # unique_together = ["first_name","last_name"]

        # containts--
        # if the condition satified it will rise an error
        constraints = [
            # models.UniqueConstraint(fields=["first_name"],name="unique_first_name_constraint"),
            # in this below example the first_name not starts with g it will rise an error
            # the name must be starts with g
            models.CheckConstraint(check=models.Q(first_name__startswith="g"), name="check_first_name_constraint")
        ]

        # verbose name is human readable label

        # see the table name in list vide and side to understand the difference
        
        verbose_name = "Person Rename"

        verbose_name_plural = "Persons Named"


class MyPerson(Person):
    class Meta:
        proxy = True

    def create(self):
        pass

# In Django, the required_db_features setting is used to specify a set of database features that must be supported by 
# the database in use. If any of the specified features are not supported, Django will raise an ImproperlyConfigured 
# exception.

# For example, suppose you have a Django project where you need certain database features to be supported by the backend 
# database. You can set required_db_features in your Django settings file (usually settings.py) like this:

# python required_db_features

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '5432',
#         'OPTIONS': {
#             'required_db_features': ['supports_transactions', 'supports_select_for_update'],
#         },
#     }
# }

# In this example, the database must support transactions and select_for_update queries. 
# If any of these features are not supported by the database, Django will raise an exception during startup.

# This setting is particularly useful when you're developing an application that relies on certain database features 
# and you want to ensure compatibility across different database backends.

# The required_db_vendor option is not a standard configuration in Django as of my last update. However, 
# hypothetically, if it were to be implemented, it could be used to enforce the use of a specific database vendor 
# for your Django project. Here's how you might use it in a hypothetical scenario:

# python required_db_vendor

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Required MySQL database vendor
#         'NAME': 'mydatabase',
#         'USER': 'mydatabaseuser',
#         'PASSWORD': 'mypassword',
#         'HOST': 'localhost',
#         'PORT': '3306',
#         'OPTIONS': {
#             'required_db_vendor': 'mysql',
#         },
#     }
# }

# In this example, the 'required_db_vendor' option is set to 'mysql', indicating that MySQL is the required database 
# vendor for the project. If another database backend is configured, Django could raise an exception during startup, 
# indicating a misconfiguration.

# However, it's important to note that as of my last update, Django doesn't have built-in support for such a feature. 
# Database vendor selection is typically done via the 'ENGINE' setting in the DATABASES configuration, and Django 
# aims to provide a database-agnostic ORM to work with different database backends.
# ---end

class LearnModel(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    # property is noting but a virutla column the value will be manipulated when we call the function
    # example
    # l = LeanModel.objects.get(id=2)
    # l.full_name #here the full name will be returned
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    # overriding the class methods or create custom class methods
    @classmethod
    def create(cls,**fields):
        lmodel = cls(first_name = fields.get("first_name"),last_name = fields.get("last_name"))
        return lmodel
    

    # The from_db method is used to create a new instance of the model from a database row. 
    # The default implementation of from_db is provided by Django, but this code overrides it 
    # with a custom implementation.

    # The from_db() method can be used to customize model instance creation when loading from the database.

    @classmethod
    def from_db(cls, db, field_names, values):
        # Default implementation of from_db() (subject to change and could # be replaced with super()).
        # concrete_fields fields are fields of database

        # basiaclly it eill used to form the models instance by using the override we can customize the field values initialization or assinging.
     
        # it will work both admin actions and orm actions

        if len(values) != len(cls._meta.concrete_fields):
            values = list(values)
            values.reverse()
            values = [

                values.pop() if f.attname in field_names else DEFERRED

                for f in cls._meta.concrete_fields

            ]

        instance = cls(*values)

        instance._state.adding = False

        instance._state.db = db

        # customization to store the original field values on the instance

        instance._loaded_values = dict(

            zip(field_names, (value for value in values if value is not DEFERRED))

        )

        print("----------instance",instance.first_name)

        return instance
    
    def refresh_from_db(self, using=None, fields=None, **kwargs):
        if fields is not None:
            fields = set(fields)
            deferred_fields = self.get_deferred_fields()
            # If any deferred field is going to be loaded
            if fields.intersection(deferred_fields):
                # then load all of them
                fields = fields.union(deferred_fields)
        print("--refresh from db",fields)
        # super().refresh_from_db(using, fields, **kwargs)
        super().refresh_from_db(using, list(fields))

class LearnValidate(models.Model):
    def get_choices():
        return {
            "L":"Large"
        }
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    uni_field = models.IntegerField(unique=True)
    learn_m = models.ForeignKey(LearnModel,on_delete=models.CASCADE)
    size = models.CharField(max_length=100,choices=get_choices)
    creation = models.DateTimeField(auto_now_add=True)
    

    # it will call only the model is used as model form and is_valid is callled in the form submission
    # it will also call in the admin portal form submission.

    # when we use model_instance.save() it will trigger the clean related methods

    # then when we use model form and use is_valid it will trigger clean related mehtods

    # When we save from adminpanel it will trigger clean realted methods.

    # def clean_fields(self, exclude: Collection[str] | None = ...) -> None:
    #     print("---clearn fields","---clearn fields")
    #     if self.age > 5:
    #         # raise ValidationError("Age can't be more than 5.")
    #         raise ValidationError(
    #                                         {
    #                                             "name": ValidationError(("Missing name."), code="required"),
    #                                             "age": ValidationError(("Invalid age."), code="invalid"),
    #                                         }
    #                                     )
    #     return super().clean_fields(exclude) 
    
    # def clean(self) -> None:
    #     print("--clean","--clean")
    #     if self.age  == 5:
    #         raise ValidationError("Age can't be 5.")
    #     if self.age == 4:
    #         raise ValidationError({"age":"kk"})
    #     return super().clean()
    
    # by default the unique error in rise by django if unique set true , we can override and give some vustom messages
    # we can define in django forms to override the behavior also
    # def validate_unique(self, exclude: Collection[str] | None = ...) -> None:
    #     if self.uni_field == 1 :
    #         raise ValidationError('unique error')
    
    # it will check any constraints like unique,check,exclusion constraints
    # not check fieldtype,mandatory.
    
    # def validate_constraints(self,exclude):
    #     pass

    #This method calls Model.clean_fields(), Model.clean(), Model.validate_unique() (if validate_unique is True), and Model.validate_constraints() (if validate_constraints is True) in that order and raises a ValidationError that has a message_dict attribute containing errors from all four stages.

    # The optional exclude argument can be used to provide a set of field names that can be excluded from validation and cleaning. ModelForm uses this argument to exclude fields that aren’t present on your form from being validated since any errors raised could not be corrected by the user.

    # Note that full_clean() will not be called automatically when you call your model’s save() method. You’ll need to call it manually when you want to run one-step model validation for your own manually created models.
    
    # def full_clean(self, exclude: Collection[str] | None = ..., validate_unique: bool = ..., validate_constraints: bool = ...) -> None:
        # print("---full clean-----------------")
        # it will call like below
        # clean_fields()
        # clean()
        # 
        # try:
        # exclude = ["age"]
        # return super().full_clean(exclude, validate_unique, validate_constraints)
        # except Exception as e:
            # to get the exact error message we can use like below
            # non_field_errors = e.message_dict[NON_FIELD_ERRORS]
            # print("--non_field_errors---",non_field_errors)
            # print("--non_field_errors---",'s')


    # get absolute url which is used in the template 
    # yes we can give the url in template without using the get_absolute_url but that is not a good practice.

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("model_detail", kwargs={"pk": self.pk})
    
  
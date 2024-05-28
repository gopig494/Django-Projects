from django.db import models
from datetime import date

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
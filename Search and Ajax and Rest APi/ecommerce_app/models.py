from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="images/")
    price = models.FloatField()
    old_price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.product_name
    
    def clean(self) -> None:
        print("---------clean ")

        return super().clean()
    
    def save(self, *args, **kwargs):
        # super(Cart,self).save(*args, **kwargs)
        super().save(*args, **kwargs)
        self.add_whhosh_data()

    def delete(self,*args,**kwargs):
        super().delete(*args,*kwargs)
        self.delete_whoosh_data()
    
    def delete_whoosh_data(self):
        from whoosh.fields import Schema,ID,TEXT
        from whoosh.index import create_in,open_dir
        import os
        from django.conf import settings
        from whoosh.qparser import MultifieldParser

        print("-----settings.BASE_DIR-----------------",locals())

        whoosh_folder_name = "whoosh_search"
        path = os.path.join(settings.BASE_DIR,whoosh_folder_name)
        if os.path.exists(path):
            ix = open_dir(path)
            with ix.writer() as writer:
                query = MultifieldParser(["id"],ix.schema).parse(str(self.id))
                # ix.delete_by_query(query)
                writer.delete_by_query(query)


    def add_whhosh_data(self):
        from whoosh.fields import Schema,ID,TEXT
        from whoosh.index import create_in,open_dir
        import os
        from django.conf import settings

        # print("-----settings.BASE_DIR-----------------",locals())

        whoosh_folder_name = "whoosh_search"
        path = os.path.join(settings.BASE_DIR,whoosh_folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            schema = Schema(name = ID(unique=True, stored=True),product_name = TEXT(stored=True))
            ix = create_in(path,schema)
        else:
            ix = open_dir(path)
        with ix.writer() as doc_writer:
            doc_writer.add_document(name = str(self.id),product_name = self.product_name)


    
class Cart(models.Model):
    customer = models.CharField(max_length=200)
    product_id = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to="images/")
    price = models.FloatField()
    old_price = models.FloatField()
    description = models.TextField()
    qty = models.IntegerField()

    def __str__(self):
        return self.product_name

    def clean(self) -> None:
        print("---------clean ")

    def full_clean(self,exclude,validate_unique):
        print("-----full clean----->")
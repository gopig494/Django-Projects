from django.db import models 
from django.db.models import Expression,Case,When,Value,F

class ExpLearn1(models.Model):
    # it wont work F not supported in db models
    # name = models.CharField(max_length=50,db_default = F("age"))
    age = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,blank=True,null=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    creation = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.age}"
    
class LearnDateDbFunc(models.Model):
    start_datetime = models.DateTimeField()
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    creation = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class DbMathFunc(models.Model):
    int_value = models.IntegerField()
    float_value = models.FloatField()
    floor_no = models.IntegerField()
    weight = models.FloatField()
    description = models.TextField()
    title = models.CharField(max_length=50)

class DBTransactions(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.title} --> {self.rating}"
    
    # def delete(self,*args, **kwargs):
    #     res = super().delete(*args, **kwargs)
    #     from django.db import transaction
    #     transaction.commit()
    #     return res
    

    class Meta:
        # db_for_read = "postgresql_db"
        app_label = "Learning_ORM_queries"
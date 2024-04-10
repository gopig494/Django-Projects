from django.db import models
import datetime

# Create your models here.



class FieldCheck(models.Model):
    auto_field = models.AutoField(primary_key=True)
    _db_col = models.BigIntegerField(db_column = "auto_db_col",default = 8)
    _blank = models.BinaryField(blank=True)
    _default = models.BooleanField(default=False)
    _help_txt = models.CharField(help_text="Help text working",max_length=10, blank = True)
    _editable_1 = models.CharField(max_length=100,editable=False,null = True, blank = True)
    _date = models.DateField(default=datetime.date.today)
    date_auto = models.DateField(null = True)
    _err_msg = models.DateTimeField(null = True,error_messages = {"null":"The fiels can't be empty."})
    # _ver_name = models.DecimalField(verbose_name="Verbose Test")
    # _vali = models.DurationField(validators=[validate_test])
    # _un = models.EmailField(unique=True,error_messages={'unique': 'The field expected to be unique'})
    # _fi = models.FileField()
    # _fl = models.FloatField()
    # _i = models.IntegerField()
    # gipadd = models.GenericIPAddressField()
    # null_b_f = models.NullBooleanField()
    # slug_f = models.SlugField(null=True)
    # ti_f = models.TimeField()
    # ti_f = models.TextField()
    # ur_f = models.URLField()
    # uu_f = models.UUIDField()

from django.core.exceptions import ValidationError

class FieldCheck2(models.Model):
    first_name = models.CharField(max_length=10,null = False, unique=True,error_messages = {"required":"Thid field can't be empty",
                                                                    "blank":"This field can't be blank",
                                                                    "invalid":"This field can't be invalid",
                                                                    "unique":"The field must be unique."})
    def clean(self):
        if not self.first_name:
            raise ValidationError({'first_name': "This field can't be empty",})



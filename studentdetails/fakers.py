import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','studentdetails.settings')

import django
django.setup()

from studentapp.models import studentdetails
from random import randint
from faker import Faker
faker=Faker()

def count(n):
    for i in range(n+1):
        sno=randint(622614114001,622614114200)
        sname=faker.name()
        saddress=faker.city()
        s_recoed=studentdetails.objects.get_or_create(student_register_no=sno,student_name=sname,student_address=saddress)
count(200)
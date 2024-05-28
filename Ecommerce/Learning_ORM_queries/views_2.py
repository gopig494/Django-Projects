from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *

def learn_meta(request):
    # all = LearnMeta.objects.all()
    # print("------------table name--",LearnMeta._meta.label)
    # print("------------table lower--",LearnMeta._meta.label.lower)

    # using different manager names and functionalities we can customize in model level
    # all = LearnMeta.custom_manager.all()
    # get_data is cutomer manager method defind in custom manager class so we can override all the methods like all,create,save,delete
    # all = LearnMeta.custom_manager.get_data()

    all = LearnMeta.objects.all()
    all = LearnMeta.qset_manager.get_all()

    all = LearnMeta._default_manager.all()  
    
    all = LearnMeta._base_manager.all()

    product = Product.objects.get(id=1)

    # learn_meta_list = product.learnmeta_set.all()

    learn_meta_list = product.get_meta.all()

    all = [LearnMeta.objects.latest()]

    # learn_meta_list = LearnMeta.objects.latest()

    print("---------learn meta---",learn_meta_list)

    # the create method is overrided and index error message is ride so we can modify as per our needs
    # manager = LearnMeta.custom_manager.create(name = "Gopi",age=16)

    return render(request,"learning_orm_queries/index.html",{"meta":all})
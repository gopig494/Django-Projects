from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *

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


def learn_model(request):
    # assume we have a database cursor and a row from a query
    from django.db import connection

    cursor = connection.cursor()

    row = ["gopi","g"]

    # create a new Book instance from the database row

    book = LearnModel.from_db(db=cursor.db, field_names=['first_name', 'last_name'], values=row)

    # print(book.first_name)  # prints the title of the book

    # print(book.last_name)  # prints the author of the book

    # book.save()

    models_dat = LearnModel.objects.get(pk=1)

    print("----first name",models_dat.first_name)

    del models_dat.first_name 

    #this will call the method refresh_from_db(using=cursor.db,fields = ["first_name"])
    print("----first name",models_dat.first_name)

    # the manual way

    # using: The database alias to use for the reload operation.
    # fields: A list of field names to reload. If None, all fields are reloaded.


    # All non-deferred fields of the model are updated to the values currently present in the database.
    # Any cached relations are cleared from the reloaded instance.

    #  Other database-dependent values such as annotations aren’t reloaded. Any @cached_property attributes aren’t cleared either


    # models_dat = models_dat.refresh_from_db(using="default",fields = ["first_name"])

    # k = LearnModel.refresh_from_db(models_dat)

    # test_update_result()

    return render(request,"learning_orm_queries/clean.html",{"form":CleanForm()})

def test_update_result():
    obj = LearnModel.objects.create(val=1)
    LearnModel.objects.filter(pk=obj.pk).update(val=F("val") + 1)
    # At this point obj.val is still 1, but the value in the database
    # was updated to 2. The object's updated value needs to be reloaded
    # from the database.
    obj.refresh_from_db()

def validate_model(request):
    val = CleanForm(request.POST)
    print("--is valid",val.is_valid())
    if val.is_valid():
        # pass
        val.save()
        # new = LearnValidate()
        # new.name = 'YY'
        # new.age = 4
        # new.uni_field = 222222222
        # # here we can call explicitly the uniqueness before hit the database
        # # by default the django call validate unique on update process so, by using below method we can validate before the data getting save. 
        # # new.validate_unique()
        # new.save() 

        # my_instance.save()  # performs an INSERT or UPDATE depending on whether the instance exists

        # my_instance.save(force_insert=True)  # always performs an INSERT, even if the instance exists

        # my_instance.save(force_update=True)  # always performs an UPDATE, even if the instance doesn't exist

        # my_instance.save(using='my_other_database')  # saves the instance to the 'my_other_database' database

        # when we using update_fields the default values set in models creation also not work

        # my_instance.save(update_fields=['name', 'email'])  # updates only the 'name' and 'email' fields

        # learn about force insert true for related models like below
        # model = LearnModel(first_name="g",last_name="dd")
        # model.save()
        # new = LearnValidate()
        # new.name = 'YY'
        # new.age = 4
        # new.uni_field = 5
        # new.learn_m = model
        # new.save(force_insert=True) 

        # dell.delete() methods returns no of matched deletes
        # we can use filter also to query and delete the entries
        dell = LearnValidate.objects.get(id=5)
        print("---dell",dell.delete())

        # delete all values
        # Entry.objects.all().delete()

    else:
        print("---form errors---",val.errors)
        form = CleanForm()
        data = LearnValidate.objects.get(pk=10)
        return render(request,"learning_orm_queries/clean.html",{"form":form,"data":data})

    return HttpResponse("ok rendered")


def get_human_readble_values(request):
    data = LearnValidate.objects.get(pk=10)

    print("------readable",data.size)
    print("------readable",data.get_size_display())
    print("------readable",data.creation)

    # it will get previous date containing data
    print("------readable",data.get_previous_by_creation())

     # it will get next date containing data
    print("------readable",data.get_next_by_creation())

    # tracks the lifecycle of the model instance.

    # when data fetched the flag adding = False and Db=db alias name

    print("----------get---adding----",data._state.adding)

    print("---------get----db---",data._state.db)

    # when data is instance is prepared but not yet saved to database the adding = True and the db = none examples below

    data = LearnValidate(name = "gopi")

    print("----------new---adding---",data._state.adding)

    print("----------new---db---",data._state.db)

    return HttpResponse("human readable objects")
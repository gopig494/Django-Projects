from django.shortcuts import render
from Learning_ORM_queries.models import *
from django.http.response import HttpResponse
import datetime
from django.db.models import Q,F,Min,Avg,Max,Sum,Count,Subquery,OuterRef,Value,JSONField,CharField, Case, When,Prefetch
from django.db.models.fields.json import KT
from django.db.models.functions import Lower,Coalesce,Upper
import django

# Create your views here.

def creating_blog(request):
    # method 1
    new_blog = Blog()
    new_blog.id = 33
    new_blog.name = "44 Travel"
    new_blog.tagline = "Around Chennai"
    new_blog.save()

    # method2
    new_blog = Blog(name = "Bike Travel",tagline = "Bike Around Chennai")
    new_blog.save()

    # method 3
    new_blog = Blog.objects.create(name = "C3 Bike Travel",tagline = "Bike Around Chennai")
    
    return render(request,"learning_orm_queries/index.html",{"info":new_blog})

def update_blog(request):
    blogs = Blog.objects.filter(name__contains = "Travel").update(name="I got bike")

    # # update forign key
    b = Blog.objects.get(pk=1)

    # # Change every Entry so that it belongs to this Blog.
    Entry.objects.update(blog=b)

    b = Blog.objects.get(pk=1)

    # Update all the headlines belonging to this Blog.

    Entry.objects.filter(blog=b).update(headline="Everything is the same")

    # using F expression
    Entry.objects.update(number_of_pingbacks=F("number_of_pingbacks") + 1)

    # if we using value from forign key field it will rise error

    Entry.objects.update(headline=F("blog__name"))

    # remove forign key relationship but the model field should set as null
    e = Entry.objects.get(id=2)
    e.blog = None
    e.save() 

    e = Entry.objects.get(id=2)
    print(e.blog)  # Hits the database to retrieve the associated Blog.
    print(e.blog)  # Doesn't hit the database; uses cached version.

    e = Entry.objects.select_related().get(id=2)
    print(e.blog)  # Doesn't hit the database; uses cached version.
    print(e.blog)  # Doesn't hit the database; uses cached version.

    # access the entry data from forign key table
    b = Blog.objects.get(id=1)
    b.entry_set.all()  # Returns all Entry objects related to Blog.

    # b.entry_set is a Manager that returns QuerySets.
    b.entry_set.filter(headline__contains="Lennon")
    b.entry_set.count()



    return HttpResponse("updated")


def get_blog(request):
    all_blog = Blog.objects.all().values()
    all_blog = Blog.objects.all().values_list("name","id")
    #and condition
    all_blog = Blog.objects.filter(name__contains = "travel",id=33).values()
    #OR condition
    all_blog = Blog.objects.filter(name__contains = "travel",id=33).values() | Blog.objects.filter(name__contains = "travel",id=69).values()
    all_blog = Blog.objects.filter(Q(name__contains = "travel")| Q(id=33) | Q(name__contains = "travel") | Q(id=69)).values()
    # like operations
    all_blog = Blog.objects.filter(name__startswith = "tada").values()
    all_blog = Blog.objects.filter(name__endswith = "travel").values()
    all_blog = Blog.objects.filter(name__contains = "travel").values() #case sesitive
    all_blog = Blog.objects.filter(name__icontains = "travel").values() #not case sesitive
    # all_blog = Blog.objects.all().filter(name__contains = "travel")
    return render(request,"learning_orm_queries/index.html",{"all_blog":all_blog})

def creating_entry(request):
    # method 1
    entry = Entry()
    entry.blog = Blog.objects.get(id=73)
    entry.headline = "Checking Entry"
    entry.body_text = "Around Chennai"
    entry.pub_date = datetime.date.today()
    entry.pub_date = datetime.date.today()
    entry.number_of_comments = 1
    entry.number_of_pingbacks = 1
    entry.rating = 3
    entry.save()
    entry.authors.add(1)
    entry.save()

    # copy and duplicate
    # many to many field are not copied we have to set it
    # which is applicable for one to one field also
    entry = Entry.objects.all()[0]  # some previous entry
    old_authors = entry.authors.all()
    entry.pk = None
    entry._state.adding = True
    entry.save()
    entry.authors.set(old_authors)
    
    # how to add and set and clear one to one fields and may to many to many fields
    entry = Entry.objects.get(pk = 1)
    entry.blog = Blog.objects.get(pk=73)
    # add will add extra values like append
    entry.authors.add(1)
    entry.authors.clear()
    # set will set like assign operator
    entry.authors.set([1,2])
    entry.save()

    return render(request,"learning_orm_queries/index.html",{"entry":entry})

def get_entry(request):
    msg = None
    # date filter
    all_entry = Entry.objects.filter(pub_date__day = 27).values() #day
    all_entry = Entry.objects.filter(pub_date__month = 4).values() #month
    all_entry = Entry.objects.filter(pub_date__year = 2024).values() #year
    all_entry = Entry.objects.filter(pub_date__exact = "2024-04-27").values()
    # grater than and less than
    all_entry = Entry.objects.filter(pub_date__gt = "2024-04-25",pub_date__lt = "2024-04-29").values()
    all_entry = Entry.objects.filter(pub_date__gte = "2024-04-26",pub_date__lte = "2024-04-28").values()
    #range
    all_entry = Entry.objects.filter(pub_date__range = ["2024-04-26","2024-04-27"]).values()
    # in
    all_entry = Entry.objects.filter(pub_date__in = ["2024-04-26","2024-04-28"]).values()
    all_entry = Entry.objects.filter(headline__contains = "check").values()
    all_entry = Entry.objects.filter(headline__isnull = False).values()
    #hour
    # from django.utils import timezone
    # all_entry = Entry.objects.filter(pub_date__hour = timezone.now().hour).values()
    # minute
    # all_entry = Entry.objects.filter(pub_date__miunte = timezone.now().minute).values()
    # second
    # all_entry = Entry.objects.filter(pub_date__second = timezone.now().minute).values()
    # hour weekday
    # current_hour = datetime.now().hour
    # day_of_week = datetime.now().weekday()
    # events = Event.objects.filter(start_time__hour=current_hour, start_time__week_day=day_of_week)
    # quarter
    all_entry = Entry.objects.filter(pub_date__quarter = 2).values()
    # using regex
    all_entry = Entry.objects.filter(headline__regex = '^[C]').values()

    # exclude
    all_entry = Entry.objects.exclude(headline__regex = '^[A]').filter(headline__contains = 'entry').values()

    # get 
    # try:
    #     all_entry = [Entry.objects.get(headline__exact = "Checking Entry")]
    # except Entry.DoesNotExist:
    #     all_entry = []
    #     msg = "does not exists"
    # except Entry.MultipleObjectsReturned:
    #     all_entry = []
    #     msg = "multiple objects retuend"
    all_entry = Entry.objects.all()[5:].values()
    # orderby
    all_entry = [Entry.objects.order_by("headline").values()[0]] #indexing
    #slicing
    all_entry = Entry.objects.order_by("headline")[:1]  
    all_entry = [Entry.objects.order_by("headline")[:1].get()]
    all_entry = Entry.objects.filter(blog = 73)

    #using forign key fields to filter the data
    all_entry = Entry.objects.filter(blog__tagline = "get django").values()

        #use containes and startswith forignkey
    all_entry = Entry.objects.filter(blog__tagline__startswith = "get django").values()
    all_entry = Entry.objects.filter(blog__tagline__contains = "get").values()
    # GET SPECIFIC FIELD ONLY
    all_entry = Entry.objects.filter(blog__tagline__contains = "get").values("rating")

    all_entry = Entry.objects.filter(blog__tagline__isnull = True).filter(blog__tagline__isnull = False)


    #using in condition
    all_entry = Entry.objects.filter(blog__tagline__in = Blog.objects.filter(tagline__contains = "get").values_list("tagline"))

    #comparing fields value using F
    all_entry = Entry.objects.filter(blog__tagline__startswith = F("headline"))

    #agggregate
    all_entry = Entry.objects.aggregate(number_of_comments = Min(2)).values()
    all_entry = [Entry.objects.aggregate(annos______= Sum('rating'))]

    #user filter and aggerigate
    all_entry = Entry.objects.filter(blog__tagline__startswith = F("headline")).aggregate(total = Sum("rating")).values()

    # using aggerigate for forigin key field
    all_entry = Entry.objects.aggregate(total = Count("blog__name")).values()

    # annotate
    all_entry = Entry.objects.values('blog').annotate(Count("blog"))

    all_entry = Entry.objects.values("pub_date__year").annotate(
                    top_rating = Subquery(
                                    Entry.objects.filter(
                                        pub_date__year = OuterRef("pub_date__year"),
                                    )
                                    .order_by("-rating")
                                    .values("rating")[:1]
                                ),
                    total_comments=Sum("number_of_comments"),)

    all_entry = Entry.objects.values("pub_date__year").annotate(
                    top_rating = Subquery(
                                    Entry.objects.filter(
                                        pub_date__year = OuterRef("pub_date__year"),
                                    )
                                    .order_by("-rating")
                                    .values("rating")[:1]
                                ),
                    total_comments=Sum("number_of_comments"),)

    all_entry = Entry.objects.values("pub_date__year").annotate(
                    top_rating =
                                    Entry.objects.filter(
                                        pub_date__year = F("pub_date__year"),
                                    )
                                    .order_by("-rating")
                                    .values("rating")[:1]
                                ,
                    total_comments=Sum("number_of_comments"),)
    
    all_entry = Entry.objects.values("pub_date__year").annotate(
                    top_rating = Max("rating"),
                    total_comments=Sum("number_of_comments"),)


    #using percentage sing to filter data
    all_entry = Entry.objects.filter(blog__tagline__contains = "%").values()

    # annotate with filters
    # MyModel.objects.annotate(num_related=Count('related_model')).filter(num_related__gt=10)

    # caching
    all_entry = Entry.objects.all().values() 
    # print("--------------all_entry",all_entry) #the database query happened here but the query happened only we evaluate it
    # print("--------------all_entry",all_entry) #here is the database query never happened it will load from queryset caching mechanism

    #caching will not happend when use indeing and slicing
    all_entry = Entry.objects.all().values() 
    all_entry = all_entry[5].values()

    # all_entry = all_entry[5].values() #again database query eill be executed

    #in this case caching will happened
    all_entry = Entry.objects.all().values() 
    all_entry = [x for x in all_entry] #here the database query will happend

    all_entry = all_entry[5].values() #here the caching data is used

    # all_entry = all_entry[5].values() #here also the caching data is used


    # async in python this is not correct // just tried
    # import time
    # async def l():
    #     for entry in enumerate(Entry.objects.all()):
    #         await time.sleep(2)
    #         print("----------count")
    # l()
    # all_entry = await Entry.objects.all().values().afirst()

    all_entry = [Entry.objects.count()]
    all_entry = [Entry.objects.exists()]
    all_entry = [Entry.objects.filter(headline__contains="travel").exists()]

    # from forn key field or onr to one or many to many field access.
    blog = Author.objects.get(pk=1)
    all_entry = blog.entry_set.all()

    
    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry,"message":msg})

def create_production(request):
    pro = Production()
    pro.values = Value(None,JSONField())
    pro.name = "Gopi"
    pro.save()

    pro = Production()
    pro.values = None
    pro.name = "Gopi"
    pro.save()

    pro = Production()
    pro.values = {"name":"Gopi","location":"comibatore",1:"nos","experience":{"software":"IT","reviews":[{"exp":"worest"}]}}
    pro.name = "Gopi"
    pro.save()

    # copy or dubplicate
    pro.pk = None
    pro._state.adding = True
    pro.save()


    # json field we can use the json key to filter the record like below location key is used

    all_entry = Production.objects.filter(values__location = "comibatore").values()

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry})


def get_production(request):
    # json field we can use the json key to filter the record like below location key is used

    all_entry = Production.objects.filter(values__location = "chennai").values()

    #nested key

    all_entry = Production.objects.filter(values__experience__software = "IT").values()

    # if the json contaies list we can use idx to filter
    all_entry = Production.objects.filter(values__experience__reviews__0__exp = "worest").values()

    # we can query null values also
    all_entry = Production.objects.filter(values__experience__software__isnull = False).values()

    # filter by another json values itself
    all_entry = Production.objects.filter(values__experience__software = KT("values__experience__software")).values()

    # using orderby

    all_entry = Production.objects.order_by("values__experience__software").filter(values__experience__software = KT("values__experience__software")).values()

    # using contains we can use but in sqlite which is not supported

    # all_entry = Production.objects.filter(values__experience__reviews__contains = [{"exp":"worest"}]).values()

    # all_entry = Production.objects.filter(values__contains = {"location":"comibatore"})

    # all_entry = Production.objects.filter(values__experience__reviews__0__contains = {"exp":"worest"}).values()

    # using contained by
    # all_entry = Production.objects.filter(values__contained_by = {"location":"comibatore"})

    # by using hey
    # all_entry = Production.objects.filter(values__has_key = "location")

    # all keys must be there
    # all_entry = Production.objects.filter(values__has_keys = ["location","name"])

    # any one of key
    # all_entry = Production.objects.filter(values__has_any_keys = ["location","name"])


    # print("---------all_entry",all_entry)

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry})

def delete_production(request):
    obj = Production.objects.get(id=3)
    obj.delete()

    obj = Production.objects.filter(id=4)
    obj.delete()

    return HttpResponse("ok")

# learning queryset api reference


def get_entry_api(request):
    # converting list
    # using all
    all_entry = list(Entry.objects.all())
    # print("------------all entry",all_entry)

    q = Blog.objects.annotate(Count("entry"))
    # The number of entries on the first blog
    # all_entry = [q[0].entry__count]
    all_entry = q.values()

    q = Blog.objects.annotate(entry_count = Count("entry"))
    all_entry = q.values()

    all_entry = Blog.objects.aggregate(entries=Count("entry")).values()

    # using alias
    all_entry = Blog.objects.alias(entries=Count("entry")).filter(entries__exact=5)
    all_entry = Blog.objects.annotate(entries=Count("entry")).filter(entries__exact=5)

    all_entry = Blog.objects.alias(entries=Count("entry")).annotate(entries=F("entries")).aggregate(Sum("entries")).values()

    
    # order by
    all_entry = Entry.objects.all().order_by("headline").values()
    for al in all_entry:
        al = Entry.objects.get(pk=al.get("id"))

    all_entry = Entry.objects.select_related().all().order_by("headline").values()
    for al in all_entry:
        al = Entry.objects.select_related().get(pk=al.get("id"))

    all_entry = Entry.objects.all().order_by("headline")
    
    # order randomly not linearly use

    all_entry = Entry.objects.all().order_by("?")

    # order by forign key field and many to many field

    all_entry = Entry.objects.all().order_by("authors__name")

    # by default it order asc but we can use - to DESC order

    all_entry = Entry.objects.all().order_by("-blog__name").values()

    # use asc and desc

    # all_entry = Entry.objects.all().order_by(Colalesce("blog__name").asc).values()

    # using case when

    all_entry = Entry.objects.annotate(
                        sorted_headline=Case(
                            When(headline__isnull=True, then=Value('')),  # Replace null values with empty string
                            default=F('headline'),  # Use headline if not null
                            output_field=CharField(),  # Specify output field type
                        )
                                ).order_by('sorted_headline')
    

    # we can use lower and upper to order by

    # all_entry = Entry.objects.order_by(Lower("headline").desc())

    # we use reverse to reverse the order
    
    all_entry = Entry.objects.all().order_by('id').reverse().values()
    all_entry = Entry.objects.all().order_by('id').values()

    all_entry = Entry.objects.distinct("pub_date").all().values()

    # we have to use order by first then use distict 
    # the distict fields must be specified in order by the fields only can speecify in distinct.

    all_entry = Entry.objects.order_by("pub_date").distinct("pub_date").all().values() 

    all_entry = Blog.objects.values("name")

    all_entry = Blog.objects.values(lower_name=Lower("name"))

    all_entry = Blog.objects.values(lower_name=Upper("name"))

    all_entry = customized_lookup_values()

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry})


def customized_lookup_values():

    # customized lookups for select query

    CharField.register_lookup(Lower)

    all_entry = Blog.objects.all().values("name__lower")

    # use group by in values itself by not using annotate

    all_entry = Blog.objects.values("entry__authors",entries = Count("entry"))

    all_entry = Blog.objects.values("entry__authors").annotate(entries=Count("entry"))

    all_entry = Blog.objects.values(entry__authors__name__lower=Lower("entry__authors__name")).annotate(entries=Count("entry"))

    all_entry = Blog.objects.values().order_by("id")
    all_entry = Blog.objects.order_by("id").values()

    # values_list

    all_entry = Blog.objects.order_by("id").values_list()

    # using flat

    all_entry = Blog.objects.order_by("id").values_list(flat=True)

    # using named

    all_entry = Blog.objects.order_by("id").values_list(named=True)

    # using get

    all_entry = Blog.objects.order_by("id").values_list().get(id=73)

    # using filter

    all_entry = Blog.objects.values_list().filter(id=73)

    # many to many field

    all_entry = Author.objects.values_list("name", "entry__headline")

    all_entry = Author.objects.values("name", "entry__headline")

    all_entry = Entry.objects.values_list("authors__name")

    # dates function

    # datetimes(field_name, kind, order='ASC', tzinfo=None)

    all_entry = Entry.objects.dates("pub_date","day", order="DESC")

    all_entry = Entry.objects.dates("pub_date","week")

    all_entry = Entry.objects.dates("pub_date","year")

    all_entry = Entry.objects.dates("pub_date","month")

    all_entry = Entry.objects.dates("pub_date","day", order="ASC")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "day")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "month")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "year")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "hour")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "minute")

    all_entry = Entry.objects.filter(headline__contains="checking").datetimes("modified", "second")

    all_entry = Entry.objects.all()
    
    # union interseaction difference

    qs1 = Author.objects.values_list("name")
    qs2 = Entry.objects.values_list("headline")
    all_entry = qs1.union(qs2).order_by("name")

    s = {1,2}
    d = {1,3}

    print(s.union(d))
    print(s.difference(d))
    print(s.symmetric_difference(d))

    all_entry = qs1.difference(qs2).order_by("name")

    # allow dublicates

    all_entry = qs1.union(qs2,all=True)

    # select related tables in sigle query 

    # Hits the database.
    e = Entry.objects.get(id=34)

    # Hits the database again to get the related Blog object.
    b = e.blog

    # Hits the database.
    e = Entry.objects.select_related("blog").get(id=34)

    # Doesn't hit the database, because e.blog has been prepopulated
    # in the previous query.
    b = e.blog

    all_entry = Entry.objects.select_related("blog").all().values()

    # it will work only for forignkeys
    # get forign key table values then the forign key forign key values.

    all_entry = Production.objects.select_related("entry__blog").all().values()

    # want to fetch all realted data values not specific
    all_entry = Production.objects.select_related().all().values()

    # for many to many field 
    all_entry = Entry.objects.prefetch_related("authors")

    all_entry = Entry.objects.prefetch_related("authors").values()

    # avoid using like it
    auths = Entry.objects.prefetch_related("authors") #hits database
    all_entry = [list(a.authors.filter(name__contains="g")) for a in auths] #hits database

    all_entry = Production.objects.prefetch_related("entries").all().values()

    #use both prefetched and select related

    all_entry = Production.objects.select_related("entry").prefetch_related("entries")

    for k in all_entry:
        entries = k.entries.all()
        # print("-------entries",entries)

    # set prefetched value none or clear them use

    all_entry.prefetch_related(None)

    # many to many field fetch specific many to many field only

    all_entry = Production.objects.prefetch_related(Prefetch("entries")).all()

    for k in all_entry:
        entries = k.entries.all()

    # use order by for many to many field

    all_entry = Production.objects.prefetch_related(Prefetch("entries",queryset = Entry.objects.order_by("-id")))

    for k in all_entry:
        entries = k.entries.all()

    # fetch the many to many field having forign key.

    all_entry = Production.objects.prefetch_related(Prefetch("entries",queryset = Entry.objects.select_related("blog"))).all()

    for k in all_entry:
        if k:
            entries = k.entries.all()
            # print('--------entries',entries)
            # if entries:
                # print("-------------entry found")
            if entries:
                for m in entries:
                    blog_id = m.blog.id
                    # print("----------blog_id",blog_id)
    
    # fetch the many to many field having many to many field.

    all_entry = Production.objects.prefetch_related(Prefetch("entries",queryset = Entry.objects.prefetch_related("authors"))).all()

    for k in all_entry:
        if k:
            entries = k.entries.all()
            # print('--------entries',entries)
            # if entries:
                # print("-------------entry found")
            if entries:
                for m in entries:
                    auths = m.authors.all()
                    # print("----------auths",auths)

    # fetch many to many field of many to many field only

    all_entry = Production.objects.prefetch_related(Prefetch("entries__authors",to_attr="menu"))

    for k in all_entry:
        if k:
            entries = k.entries.all()
            if entries:
                for m in entries:
                    auths = m.authors.all()
                    # print("----------auths",auths)


    # using filter in prefetch

    all_entry = Production.objects.prefetch_related(Prefetch("entries",queryset=Entry.objects.filter(headline__startswith="c"),to_attr="menu"))

    for k in all_entry:
        if k:
            entries = k.menu
            for a in entries:
                # print("----------a",a.headline)
                # print("----------a",a.blog)
                pass

    # using only # fetch necessary fields only

    all_entry = Production.objects.prefetch_related(Prefetch("entries",queryset=Entry.objects.only("headline").filter(headline__startswith="c"),to_attr="menu"))

    for k in all_entry:
        if k:
            entries = k.menu
            for a in entries:
                print("----------a",a.headline)
                print("----------a",a.blog)
    

    # fetch data from different database by using the keyword 'using

    # # Both inner and outer queries will use the 'replica' database
    # Restaurant.objects.prefetch_related("pizzas__toppings").using("replica")
    # Restaurant.objects.prefetch_related(
    # Prefetch("pizzas__toppings"),).using("replica")

    # # Inner will use the 'replica' database; outer will use 'default' database
    # Restaurant.objects.prefetch_related(
    # Prefetch("pizzas__toppings", queryset=Toppings.objects.using("replica")),)

    # # Inner will use 'replica' database; outer will use 'cold-storage' database
    # Restaurant.objects.prefetch_related(
    # Prefetch("pizzas__toppings", queryset=Toppings.objects.using("replica")),).using("cold-storage")'
    
    # when we call the prefetch related internally the method prefetch_related_objects is called to fetch related objects

    # FilteredRelation

    # from django.db.models import FilteredRelation, Q
    # Restaurant.objects.annotate(   
    #      pizzas_vegetarian=FilteredRelation(
    #          "pizzas",
    #          condition=Q(pizzas__vegetarian=True),
    #      ),
    #  ).filter(pizzas_vegetarian__name__icontains="mozzarella")

    # # If there are a large number of pizzas, this queryset performs better than:

    # Restaurant.objects.filter(
    #     pizzas__vegetarian=True,
    #         pizzas__name__icontains="mozzarella",
    #  )

 
    return all_entry  


# how to use custom sql with django orm which means combination of sql and django ORM

def learn_extra(request):

    # adding count of entries to each field

    all_entry = Entry.objects.extra(select={"count_entry":"SELECT COUNT(id) FROM Learning_ORM_queries_entry"}).values()

    # mixing the orm field and then the subquery field in subquery where condition

    all_entry = Entry.objects.extra(select={"count_entry":"SELECT COUNT(id) FROM Learning_ORM_queries_blog WHERE id = Learning_ORM_queries_entry.blog_id"}).values()

    # using select params to pass a value the the where condition
    
    all_entry = Entry.objects.extra(select={"count_entry":"""
                                        SELECT 
                                            COUNT(id) FROM Learning_ORM_queries_blog 
                                        WHERE 
                                            name = %s """},
                                    select_params=('finally',)).values()
    
    # two subquery

    all_entry = Entry.objects.extra(select={"count_entry":"""
                                        SELECT 
                                            COUNT(id) FROM Learning_ORM_queries_blog 
                                        WHERE 
                                            name = %s """,
                                            "ee":"""
                                        SELECT 
                                            COUNT(id) FROM Learning_ORM_queries_blog 
                                        WHERE 
                                            name = %s """},
                                    select_params=('finally','finally',)).values()

    # add additional where condition to the ORM 

    # this is the example of how we use OR and AND condition in where clause

    all_entry = Entry.objects.extra(where=["headline LIKE '%2%' OR headline = 'Checking Entry'","number_of_comments = 1"]).values('headline')

    # using Order by

    all_entry = Entry.objects.extra(order_by=["-rating"]).values('headline','rating')

    # adding dynamic where condition

    all_entry = Entry.objects.extra(where=["headline=%s"],params=["Checking Entry",]).values('headline','rating')


    # rawsql

    # qs.annotate(val=RawSQL("select col from sometable where othercol = %s", ('s',)))

    # learn about defer 

    # defer is used to delay the sql excution for particular field

    # then when the execution start mean when you tring to access it like below

    all_entry = Entry.objects.defer("headline", "body").values()

    # all_entry.headline  #here the additional sql query executed

    # use defer for related models

    all_entry = Blog.objects.select_related().defer("entry__headline", "entry__body_text")

    # cancel or remove all the defer we can use
    
    all_entry =all_entry.defer(None)

    # learn about only

    #it wii only load the headline and bodytext when executed another important info is we can access another fields

    # like blog,rating the difference is the extra sql query excuted when we trying to use the blog and rating

    all_entry = Entry.objects.only("headline", "body_text").values()

    # the id also fetched which means three fields are fetched
    all_entry = Entry.objects.only("headline", "body_text").values('id')

    # in this case the lase only fields only will be fetched and cached which mean id field only cached
    all_entry = Entry.objects.only("headline", "body_text").only('id')

    # dffer vs only

    # When calling save() for instances with deferred fields, only the loaded fields will be saved. See save() for more details.

    # assume the entry table having only the headline and body_text field.

    # so here the first line the two fields defer so the id field data only fetched same in line 2

    all_entry = Entry.objects.defer("headline", "body_text")
    all_entry = Entry.objects.only("id")

    # Final result is that everything except "headline" is deferred.
    Entry.objects.only("headline", "body_text").defer("body_text")

    # Final result loads headline immediately.
    Entry.objects.defer("body_text").only("headline", "body_text")

    # here the there is not values cached during evaluation the sql excute and get all the field values.

    # When using defer() after only() the fields in defer() will override only() for fields that are listed in both.

    all_entry = Entry.objects.only().values()

    # learn the using function

    # queries the database with the 'default' alias.
    all_entry = Entry.objects.all()

    # queries the database with the 'backup' alias
    # all_entry = Entry.objects.using("backup")

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry})

def lock_transaction(request):
    from django.db import transaction
    entry_all = []
    # general method
    all_entry = Entry.objects.select_for_update().all()
    with transaction.atomic():
        for entry in all_entry:  # here the all matched querset rows are locked which means they are not availbel to change the data or access
            # if the query is already locked by using the same method in another call , the query will be blocked untill the lock is released
            pass
        
        
    # if the query is already locked by using the same method in another call , the query will be '''**not**''' blocked untill the lock is released
    # like its normal flow to access the data
    # if we trying to access in another method the ''' DatabaseError  ''' will rise like below
    # for example the query is locked by another fuction and here we are using nowait = true so the below code attempt to execute the code in this case the datbase error will rised
    all_entry = Entry.objects.select_for_update(nowait=True).all()
    with transaction.atomic():
        for entry in all_entry:  
            pass
    
    # by refer the previous scnario if you dont want to rise database error we can use like below
    all_entry = Entry.objects.select_for_update(skip_locked=True).all()
    with transaction.atomic():
        for entry in all_entry: 
            pass
    
    # if we use like below the '''values error wil rise'''
    # nowait-true,skip_locked=true together
    # all_entry = Entry.objects.select_for_update(nowait=True,skip_locked=True).all()
    # with transaction.atomic():
    #     for entry in all_entry: 
    #         pass
    
    #  lock forign key models 
    all_entry = Entry.objects.select_for_update(of=("self","blog_ptr")).all()
    with transaction.atomic():
        for entrys in all_entry: 
            entry_all.append(entrys)

    # apply lock for single field
    all_entry = Entry.objects.select_for_update("headline").select_related().all()

    # we can't use the 'select for update ' for null type fields
    # to avoid the error we can use
    all_entry = Entry.objects.select_for_update("headline").select_related().exclude(headline = None).all()

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

def and_or(request):
    entry_all = []
    # and condition
    all_entry = Entry.objects.filter(headline__startswith="C").filter(rating = 3)
    all_entry = Entry.objects.filter(headline__startswith="C",rating = 3)

    all_entry = Entry.objects.filter(Q(headline__startswith="C") & ~Q(rating = 3))
    all_entry = Entry.objects.filter(headline__startswith="C") & Entry.objects.filter(rating = 3)

    # or condition

    all_entry = Entry.objects.filter(Q(headline__startswith="C") | Q(rating = 3))
    all_entry = Entry.objects.filter(headline__startswith="C") | Entry.objects.filter(rating = 3)

    # xor

    # Model.objects.filter(x=1) ^ Model.objects.filter(y=2)
    # from django.db.models import Q

    # Model.objects.filter(Q(x=1) ^ Q(y=2))

    # learn about get

    # we can fetch many to many field and forigkey values in get

    all_entry = Entry.objects.get(pk = 34)

    # print('???????????????????????????/////////////////////////////////////',all_entry.authors.all())
    
    # but in filter we ca't get the many to many field values

    all_entry = Entry.objects.filter(pk = 34)

    # print('???????????????????????????/////////////////////////////////////',all_entry.authors.all())

    # if we want to get many to many field in filter we need to use like below

    all_entry = Entry.objects.filter(pk = 34).get()

    # print('???????????????????????????/////////////////////////////////////',all_entry.authors.all())

    # this is the asynchronus call

    all_entry = [Entry.objects.aget(pk = 34)]

    print('???????????????????????????/////////////////////////////////////',all_entry)

    # if we get more than one record the multiple objects returns error eill rise 
    # if we do not get any values it will rise the doesnot exists error

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

def crud(request):
    entry_all = []
    # get
    all_entry = [Entry.objects.get(pk = 34)]
    # async version
    # it will not wait to fetch the data so there no data print in index.html
    all_entry = [Entry.objects.aget(pk = 34)]

    # create

    # all_entry = Blog.objects.create(name="Soga kathai",tagline="bhai")

    # async version #this is not correct way just trying
    # async def create_blog():
    #     globals()["all_entry"] = await Blog.objects.acreate(name="async Soga kathai",tagline="async bhai")
    # create_blog()

    # another way to create
    # when use create a primary key with ourself the force insert will be useful 
    # the primary key 1 alreay exists by default the save method will update the record not insert
    # in this above swtchuation we can use the forcew insert true it will rise unique contraints error so we canm handle the exception
    # and generate the new primary ley
    all_entry = Blog(name="force insert Soga kathai",tagline="force insert bhai",pk=1)
    # all_entry.save(force_insert=True)
    try:
        all_entry = Blog(name="force insert Soga kathai",tagline="force insert bhai",pk=1)
        all_entry.save(force_insert=True)
        all_entry = [all_entry]
    except django.db.utils.IntegrityError:
        pass

    # get or create method
    # in this below example the methos having filters having data in database so there is no record created in database
    # so this method only getting value from database

    obj,created = Blog.objects.get_or_create(name="force insert Soga kathai",tagline="force insert bhai")
    # print("????????????????????????????????????????????????obj",obj)
    # print("????????????????????????????????????????????????-------------------create",created)

    # in this below method a new record is created 
    obj,created = Blog.objects.get_or_create(name="get or set Soga kathai",tagline="get or set force insert bhai")
    # print("????????????????????????????????????????????????obj",obj)
    # print("????????????????????????????????????????????????-------------------create",created)

    # we can use filter and or conditions

    # obj,created = Blog.objects.filter(Q(name="okok") & Q(tagline="2okok") | (Q(name="p"))).get_or_create(name="lkk Soga kathai",tagline="lkk force insert bhai")

    # if multiple objects found for given filter the multiple objects return error will rise

    # using default keyword
    # default is used to set value when no match found which means the default is used to set value when new object ic created
    # it won't be used to filter instean it will used to set values only
    obj,created = Blog.objects.get_or_create(name="get or set Soga kathai",tagline="get or set force insert bhai",defaults={"name":"default word"})
    # print("????????????????????????????????????????????????obj",obj)

    # what happedn when we have default field alos for that we can use like below

    # obj,created = Blog.objects.get_or_create(name="get or set Soga kathai",tagline="get or set force insert bhai",defaults__exact = "d",defaults={"name":"default word"})
    # print("????????????????????????????????????????????????obj",obj)

    # we can use get_or_create for related models like many to many field 

    obj = Entry.objects.get(pk=33)
    obj.authors.get_or_create(name = "Govind")

    # we can use async version of it
    # use aget_or_create()

    # learn about update_or_create

    # in this example the defaults is used to update the filed value if match is found 
    # and the create default is used to if there is no match found create the record with values mentioned in it.
    obj,created = Blog.objects.update_or_create(name="get or set Soga ksathai",defaults={"name":"updated called"},create_defaults = {"name":"create defaults"})
    print("????????????????????????????????????????????????obj",obj)
    print("????????????????????????????????????????????????-------------------create",created)

    # Asynchronous version: aupdate_or_create()

    # bulk update

    # the trigger events not will be trigger example save,pre_save,post_save

    # not used to update many to many field values

    # all_entry = Blog.objects.bulk_create(
    #     [
    #         Blog(name="Kailasam"),
    #         Blog(name="Sankar")
    #     ]
    # )

    # ignore conflicts

    # if the name is unique then it throw unique constraint error

    # all_entry = Author.objects.bulk_create(
    #     [
    #         Author(name="Kailasam",email="test@gmail.com"),
    #         Author(name="Sankar",email="test@gmail.com")
    #     ],
    #     ignore_conflicts = False
    # )

    # if i give the 'ignore_conflicts = true' it will ignore the record which is create any erorr like below

    # if i trying to insert the below record the unique error rise by default but in the case the error will not rise and the record also not will be inserted

    all_entry = Author.objects.bulk_create(
        [
            Author(name="Kailasam",email="test@gmail.com"),
            Author(name="Sankar",email="test@gmail.com")
        ],
        ignore_conflicts = True
    )
  
    # The batch_size parameter controls how many objects are created in a single query. 

    all_entry = Author.objects.bulk_create(
        [
            Author(name="Kailasams",email="test3@gmail.com"),
            Author(name="Sankars",email="test4@gmail.com")
        ],
        ignore_conflicts = True,batch_size=1
    )
  
    # update_conflicts #explore the unique and update fields

    all_entry = Author.objects.bulk_create(
        [
            Author(name="Kailasams",email="test3@gmail.com"),
            Author(name="Sankars",email="test4@gmail.com")
        ],
        update_conflicts = True,update_fields=None,unique_fields = None
    )


    # learn about bulk_update

    # the trigger events not will be trigger example save,pre_save,post_save

    # bulk_update(objs, fields, batch_size=None)

    # this is not correct way to update explore when its required

    all_entry = Author.objects.bulk_update(
        [
            Author.objects.filter(name="Kailasams",email="test3@gmail.com"),
            Author.objects.filter(name="Sankars",email="test4@gmail.com")
        ],fields=["name","email"]
    )

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

def more_functions(request):
    entry_all = []

    # using count

    all_entry = [Author.objects.count()]

    # using filter together

    all_entry = [Author.objects.filter(name__contains="s").count()]

    # in bulk by using the primary keys is more efficient than filter()

    # in_bulk(id_list=None, *, field_name='pk')

    # it will return key value dictories

    all_entry = Author.objects.in_bulk([6])

    # print("-----------------------in bulk",all_entry)

    all_entry = Author.objects.in_bulk([6,15])

    print("-----------------------in bulk",all_entry)

    # by default it will filter by pk but we can change it like below

    all_entry = Author.objects.in_bulk(["Gopi"],field_name="name")

    print("-----------------------in bulk",all_entry)

    # we can use distinct together
    # sqlite not support this

    # all_entry = Author.objects.distinct("name").in_bulk(field_name="name")

    # if we give in_bulk only , it will fetch all the records

    all_entry = Author.objects.in_bulk()

    # iterator(chunk_size=None)

    # if we have a queryset which evaluated once like print(queryset) it wont do sql again when we trying to evaluate again like print(queryset)

    # for example

    all_entry = Author.objects.all()  

    print("-------all authors",all_entry) #sql query will be execured

    print("-------all authors",all_entry) #here is no any sql query executed intead of it the caching value will be loaded

    # so if you want to fetch the value from db not from caching like above
    # we can use the iterator

    # Note that using iterator() on a QuerySet which has already been evaluated will force it to evaluate again, 

    all_entry = Author.objects.all()  

    # 10 rows will be queried
    print("-------all authors",all_entry.iterator(chunk_size=10)) #sql query will be execured

    # 15 rows will be queried
    print("-------all authors",all_entry.iterator(chunk_size=15)) #sql query will be execured

    # we can alos use related models

    all_entry = Entry.objects.all().select_related()

    # 15 rows will be queried
    print("-------all authors",all_entry.iterator(chunk_size=15)) #sql query will be execured

    # providing no value for chunk_size will result in Django using an implicit default of 2000.

    # using latest

    # it will give the latest data record

    all_entry = [Entry.objects.latest("pub_date")]

     # it will give the oldest data record

    all_entry = [Entry.objects.latest("-pub_date")]

    # if we two datas are same we can add one more field to compare like below

    # first it will look into oubdata if the pub date same meas it compare the mod data like same way

    # if there is no values fount doesnot found error will rise

    all_entry = [Entry.objects.latest("-pub_date","mod_date")]

    # earliest(*fields) 

    all_entry = [Entry.objects.earliest("-pub_date","mod_date")]

    # using first

    # it will fetch vslue order by primary key

    all_entry = [Entry.objects.first()]

    # bothare the same like above and below

    all_entry = [Entry.objects.all()[0]]

    # we can use order by

    all_entry = [Entry.objects.order_by("rating").first()]

    # the same thing we can use for last

    all_entry = [Entry.objects.order_by("rating").last()]

    # aggerigate function

    all_entry = [Entry.objects.aggregate(name = Count("id"))]

    # exists

    # in this below query it will execute and give 1 or zero and also no data will be in cache

    all_entry = [Entry.objects.filter(headline__contains="c").exists()]
    
    # exe

    entry = Entry.objects.filter(headline__contains="c")

    print("-------------------entry exists",entry.exists()) # here sql query executed to fetch the data

    print("------------------------entry data",entry.values()) #here sql queryy executed to fetch the data

    # bool

    all_entry = [bool(Entry.objects.filter(headline__contains="c"))]

    # contains(obj)

    # instead of using like {"ss":"s"}<queryset> and in 

    # if obj in queryset: we can use below it will improve the performance

    # queryset.contains(obj) #efficient way to find a obj in or not

    #  update(**kwargs)¶

    # here it will update the filterd all records with update value like below

    # only restriction on the QuerySet that is updated is that it can only update columns in the model’s main table

    # Entry.objects.update(blog__name="foo")  # Won't work!

    # it will return no of affected rows

    # Finally, realize that update() does an update at the SQL level and, thus, does not call any save() methods on your models, nor does it emit the pre_save or post_save signals

    queryset = Entry.objects.filter(body_text="Around Chennai")

    if queryset.exists():
        queryset.update(headline="Updated")
        # we can use order by then update it
        queryset.order_by("headline").update(headline="Updated")
    
    # delete()

    # instantly it will be deleted

    # queryset = Entry.objects.filter(id=34).delete()

    # The delete() method does a bulk delete and does not call any delete() methods on your models. It does, however, emit the pre_delete and post_delete signals for all deleted objects (including cascaded deletions).

    # we can print what query will be executed when we use wuery set by using explain fundtion

    # explain()¶

    queryset = Entry.objects.filter(body_text="Around Chennai").explain()

    # we can format the output like below
    
    # not supported in sqllite database
    
    # queryset = Entry.objects.filter(body_text="Around Chennai").explain(format="JSON")

    # queryset = Entry.objects.filter(body_text="Around Chennai").explain(verbose=True, analyze=True)

    print("-------------------queryset",queryset)

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

def diff_filters(request):
    entry_all = []

    """exact"""

    # exact #it is case sensitive

    # which like == if python , we dont't need to use it simple use = for that

    # it will only match Updated only

    all_entry = Entry.objects.filter(headline__exact="Updated") .values()

    # iexact case intesive #it will filter the text are in both upper and lower

    # it will match like JOHN.John,john

    all_entry = Entry.objects.filter(headline__iexact="Updated") .values()

    """contains and icontains"""

    # it is like %kkk% operation in sql
    
    all_entry = Entry.objects.filter(headline__contains="Updated") .values()

    all_entry = Entry.objects.filter(headline__icontains="Updated") .values()

    """ in,in """

    # both are the same

    # there is no 'iin' method

    all_entry = Entry.objects.filter(headline__in=[1,2,3]) .values()

    all_entry = Entry.objects.filter(headline__in="123") .values()

    # we can use dynamic query like

    all_entry = Entry.objects.filter(blog__in=Blog.objects.all()) .values()

    # the correct way to optimize is

    all_entry = Entry.objects.filter(blog__in=Blog.objects.all().values("id")) .values()

    """ gt,gte,lt,lte """

    all_entry = Entry.objects.filter(rating__lt=3) .values()

    all_entry = Entry.objects.filter(rating__lte=3) .values()

    all_entry = Entry.objects.filter(rating__gt=3) .values()

    all_entry = Entry.objects.filter(rating__gte=Blog.objects.all().values("id")).values()

    """ startswith,endswith """

    all_entry = Entry.objects.filter(headline__startswith = "u").values()

    all_entry = Entry.objects.filter(headline__endswith = "d").values()

    """ istartswith,iendswith """

    all_entry = Entry.objects.filter(headline__istartswith = "u").values()

    all_entry = Entry.objects.filter(headline__iendswith = "d").values()

    """ range """

    all_entry = Entry.objects.filter(rating__range = (1,10)).values()

    """ date,year,iso_year,month,day,week,week_day,iso_week_day,quarter,time,hour,minute,second """

    # this is only used in datatimefield

    all_entry = Entry.objects.filter(modified__date = "2024-04-30").values()

    # both datetime and date field

    all_entry = Entry.objects.filter(modified__year = "2024").values()

    all_entry = Entry.objects.filter(pub_date__year = "2024").values()

    all_entry = Entry.objects.filter(pub_date__year__gte = "2024").values()

    # iso_year

    all_entry = Entry.objects.filter(modified__iso_year = "2024").values()

    # month

    all_entry = Entry.objects.filter(modified__month__lte = "05").values()

    # day like june 3 @almost like data filter

    all_entry = Entry.objects.filter(modified__day = 30).values()

    # week

    all_entry = Entry.objects.filter(modified__week__gte = 15).values()

    # weekday

    # iso_week_day

    # Note this will match any record with a pub_date that falls on a Monday (day 1 of the week), 
    # regardless of the month or year in which it occurs. Week days are indexed with day 1 being Monday 
    # and day 7 being Sunday

    all_entry = Entry.objects.filter(modified__week_day = 3).values()

    # quarter

    all_entry = Entry.objects.filter(modified__quarter =2).values()

    # time

    all_entry = Entry.objects.filter(modified__time = datetime.time(1, 49,35)).values()

    # hour

    all_entry = Entry.objects.filter(modified__hour = 1).values()

    # minute

    all_entry = Entry.objects.filter(modified__minute = 49).values()

    # second

    all_entry = Entry.objects.filter(modified__second = 35).values()

    """ isnull """

    all_entry = Entry.objects.filter(modified__isnull = True).values()

    """ regext  """

    all_entry = Entry.objects.filter(modified__regex = "1").values()

    " Aggerigate functions "

    # using output field

    """ Sum,Count,Avg,Min,Max,StdDev,Variance """

    all_entry = Entry.objects.aggregate(e_count=Sum("rating",output_field = CharField()))

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

def revise(request):
    # create many to many field table record by parent table orm
    entry_all = []
    all_entry = Entry.objects.get(id=33)
    all_entry.authors.create(name='Indian3',through_defaults={"email": "123r@gmail.com"})
    # it will unselected the specified value from the master table.
    all_entry.authors.remove(54)
    all_entry.save()
    all_entry = [all_entry]
    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry or entry_all})

# from datetime import timedelta
# Entry.objects.filter(mod_date__gt=F("pub_date") + timedelta(days=3))
# Blog.objects.filter(pk__gt=14)


# To compare two model instances, use the standard Python comparison operator, the double equals sign: ==. Behind the scenes, that compares the primary key values of two models.

# Using the Entry example above, the following two statements are equivalent:

# >>> some_entry == other_entry
# >>> some_entry.id == other_entry.id

# If a model’s primary key isn’t called id, no problem. Comparisons will always use the primary key, whatever it’s called. For example, if a model’s primary key field is called name, these two statements are equivalent:

# >>> some_obj == other_obj
# >>> some_obj.name == other_obj.name


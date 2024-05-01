from django.shortcuts import render
from Learning_ORM_queries.models import *
from django.http.response import HttpResponse
import datetime
from django.db.models import Q,F,Min,Avg,Max,Sum,Count,Subquery,OuterRef,Value,JSONField,CharField, Case, When,Prefetch
from django.db.models.fields.json import KT
from django.db.models.functions import Lower,Coalesce,Upper

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
    
    # how to add and set and clear one to one fields and may tot many tot many fields
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
    all_entry = Entry.objects.using("backup")

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry})
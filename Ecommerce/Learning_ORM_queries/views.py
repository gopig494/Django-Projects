from django.shortcuts import render
from Learning_ORM_queries.models import *
from django.http.response import HttpResponse
import datetime
from django.db.models import Q,F,Min,Avg,Max,Sum,Count,Subquery,OuterRef

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

    all_entry = all_entry[5].values() #again database query eill be executed

    #in this case caching will happened
    all_entry = Entry.objects.all().values() 
    all_entry = [x for x in all_entry] #here the database query will happend

    all_entry = all_entry[5].values() #here the caching data is used

    all_entry = all_entry[5].values() #here also the caching data is used

    async def l():
    
        async for entry in Entry.objects.all():
            pass

    return render(request,"learning_orm_queries/index.html",{"all_entry":all_entry,"message":msg})
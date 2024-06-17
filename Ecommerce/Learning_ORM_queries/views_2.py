from django.http.response import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
from django.db import connection

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

    data.get_values()

    return HttpResponse("human readable objects")

def raw_sql_learning(request):

    # using objects raw

    data = LearnValidate.objects.raw("SELECT * FROM Learning_ORM_queries_learnvalidate WHERE name = 'Gopi'")
    for each_rec in data:
        print("--each_rec---",each_rec.pk)
    # learn about alias
    data = LearnValidate.objects.raw("SELECT name AS l_name,age AS age_no,id FROM Learning_ORM_queries_learnvalidate WHERE name = 'Gopi'")
    for each_rec in data:
        print("--each_rec----alias--",each_rec.l_name)
    # using djangos translate
    name_map = {"name":"l_name","age":"age_no"}
    data = LearnValidate.objects.raw("SELECT name,age,id FROM Learning_ORM_queries_learnvalidate WHERE name = 'Gopi'",translations=name_map)
    for each_rec in data:
        print("--django translation----alias--",each_rec.l_name)
    # defered field is fetched only when we trying to access not by doing the raw sql or query set
    # examples last_name is defer field so it will fetxh when we trying to access it
    # >>> for p in Person.objects.raw("SELECT id, first_name FROM myapp_person"):
    # ...     print(
    # ...         p.first_name,  # This will be retrieved by the original query
    # ...         p.last_name,  # This will be retrieved on demand
    # ...     )
    # ...
    # John Smith
    # Jane Jones

    # passing params to raw sql

    data = LearnValidate.objects.raw("SELECT name,age,id FROM Learning_ORM_queries_learnvalidate WHERE name = %s",['Gopi'])

    data = LearnValidate.objects.raw("SELECT name,age,id FROM Learning_ORM_queries_learnvalidate WHERE name = %(name)s",{"name":'Gopi'})

    for each_rec in data:
        print("--params--dict--alias--",each_rec.name)

    # using connections and cursor

    with connection.cursor() as cursor:
        cursor.execute(" SELECT * FROM Learning_ORM_queries_learnvalidate")
        
        # when using dynamic params do not include '' quotes in query like '%s' use only %s
        
        cursor.execute(" SELECT * FROM Learning_ORM_queries_learnvalidate where name=%s",['Gopi'])

        # row = cursor.fetchone()
        all_row = cursor.fetchall()
        # many_row = cursor.fetchmany()
        # print("---fetch one---",row)
        print("---fetch all--",all_row)
        # print("---fetch many_row--",many_row)

        def map_dict(cursor):
            columns = [col[0] for col in cursor.description]
            # print("----columns-----",columns)
            return [dict(zip(columns,row)) for row in all_row]

        key_val = map_dict(cursor)

        print("---key---val---",key_val)
    
    # when using multiple database we can use the database alias name to coonect like below

    # with connection["db alias name"].cursor() as cursor:

    # this is how multiple databse configured in settings.py

    # and the 'default' and 'users' is the database names

#     DATABASES = {
#     "default": {
#         "NAME": "app_data",
#         "ENGINE": "django.db.backends.postgresql",
#         "USER": "postgres_user",
#         "PASSWORD": "s3krit",
#     },
#     "users": {
#         "NAME": "user_data",
#         "ENGINE": "django.db.backends.mysql",
#         "USER": "mysql_user",
#         "PASSWORD": "priv4te",
#     },
# }

    

    return HttpResponse("human readable objects")


def learn_sql_store_procedure(request):

    # if we have store procedure in our databse already we can call by below methods

    with connection.cursor() as cursor:
        cursor.callproc("procedure name",["args"])

    return HttpResponse("human readable objects")

def model_inheritance(request):

    cust = BankCustomer.objects.all()

    for c in cust:
        print("---c---",c.state_name)
        print("---c---",c.country_name)
        print("---c---",c.customer_name)
    
    va = LearnValidate.objects.all()
    for v in va:
        print("---va--m",v.learning_orm_queries_shopcustomer_related.all())
        # print("---va--m",v.shopcustomer_set.all())

    iphone = Iphone.objects.all()
    print("---repr",repr(iphone))
    print("---print",iphone)
    for v in iphone:
        print("---iphone--",v.id)

    iphone = IphoneModel.objects.get(id=1)
    print("---iphone-related-",v.iphone.id)

    # we can access the proxy xustom defined methods by the manager as well as creating objects for the model

    # the crud operation also can able to do by the proxy model

    proxy = ChildProx(proxy_name="kk",order_no=1)
    proxy.save()

    proxy = ChildProx.objects.get(id=1)

    proxy.validate_order_no()

    # import asyncio

    # asyncio.run(main())

    print("----async function")


    return HttpResponse("test model inheritance")

# async def main():
#     await astnc_pro()

# async def astnc_pro():
#     import asyncio
#     iphone = Iphone.objects.all()
#     print("---repr",repr(iphone))
#     async for v in iphone:
#         asyncio.sleep(10)
#         print("---ipho<<>>><>ne--",v.id)


def learn_aggerigation(request):

    # 1.count

    count = ProxyLearn.objects.count()

    print("---count without filter filter",count)

    filter_count = ProxyLearn.objects.filter(proxy_name = 'porur').count()

    print("---count filter",filter_count)


    # 2.AVG

    from django.db.models import Avg

    avg = ProxyLearn.objects.aggregate(Avg("order_no",default = 0))

    print("----avg without filter---",avg) #'order_no__avg': 1.0666666666666667}

    avg_filter = ProxyLearn.objects.filter(proxy_name="porur").aggregate(Avg("order_no",default = 0))

    print("----avg filter---",avg_filter) #{'order_no__avg': 1.0}


    # 3.Max

    from django.db.models import Max

    max = ProxyLearn.objects.aggregate(Max("order_no",default = 0))

    print("----max without filter---",max) #{'order_no__max': 2}

    max_filter = ProxyLearn.objects.filter(proxy_name="porur").aggregate(Max("order_no",default = 0))

    print("----max filter---",max_filter) # {'order_no__max': 1}

    # 4.Min

    from django.db.models import Min

    min = ProxyLearn.objects.aggregate(Min("order_no",default = 0))

    print("----min without filter---",min) #{'order_no__min': 1}

    min_filter = ProxyLearn.objects.filter(proxy_name="porur").aggregate(Min("order_no",default = 0))

    print("----min filter---",min_filter) # {'order_no__min': 1}

    # doing some arethematic operation

    from django.db.models import FloatField

    res = ProxyLearn.objects.aggregate(resp = Min("order_no",output_field = FloatField(),default = 0) - Avg("order_no"))

    print("---arthematic ope--",res) #{'resp': -0.06666666666666665}

    # above and below codes are same

    res = ProxyLearn.objects.aggregate(resp = Min("order_no") - Avg("order_no"))

    print("---arthematic ope--",res)

    # annotate vs aggeregate

    from django.db.models import Sum

    # aggregate is a method that computes a single value from a queryset, often by grouping the results. 
    # It returns a dictionary with the aggregated values.

    # annotate is a method that adds a new attribute to each object in a queryset, based on a calculation or aggregation. 
    # It allows you to compute a value for each object in the queryset, without grouping the results.

    # supposse if consider order_no as a product price then we have to calculate discount for each price
    # how could we done is we can simple annotate then give the discount percentage like below 

    anno = ProxyLearn.objects.annotate(discount_order_no = F("order_no") * 10/100 )

    for an in anno:
        print("---an",an.discount_order_no)

    # use annotate with aggregate function

    # if you not able to unserstand see the proxylearn model

    anno = ProxyLearn.objects.annotate(avg_rating = Avg("review__rating"),total_rating = Sum("review__rating"))


    for an in anno:
        print("---an--2",an.avg_rating)
        print("---an--2",an.total_rating)

    # another way to use annotate using when case

    from django.db.models import Case,When

    anno = ProxyLearn.objects.annotate(pub = Case(
                When(proxy_name="porur",then="proxy_name"),
                default="proxy_name"
    ))

    # These are just a few examples of how you can use annotate to add new attributes to a queryset in Django's ORM. The possibilities are endless!

    # end

    for an in anno:
        print("---an--3",an.pub)

    agg = ProxyLearn.objects.aggregate(total = Sum("order_no")) #total is custom key

    print("--agg",agg)

    # >>> from django.db.models import Avg, Max, Min
    # >>> Book.objects.aggregate(Avg("price"), Max("price"), Min("price"))
    # {'price__avg': 34.35, 'price__max': Decimal('81.20'), 'price__min': Decimal('12.99')}

    # we can filter the count of distinct values like example below

    from django.db.models import Count

    unique_count = ProxyLearn.objects.aggregate(uni_count = Count("order_no",distinct=True))

    print("---unique count--",unique_count)

    # use aggerigation for relationship fields like many to many fields

    # it will aggeregate the whole relationship fields values so the output will be object not list like single aggeregation

    anno = ProxyLearn.objects.aggregate(avg_rating = Avg("review__rating"),total_rating = Sum("review__rating"))

    print("----anno use agg for manyt to many----",anno)

    # we can use any filters lookup in aggerregation like filter indeep like below examples


    anno = Rating.objects.aggregate(avg_order_no = Avg("proxylearn__order_no"),total_order_no = Sum("proxylearn__order_no"))

    print("----anno use ageg to relationship fields----",anno)


    # using filter and exclude in aggergations and annotate function

    filter_anno = ProxyLearn.objects.filter(proxy_name="porur").annotate(avg_rating = Avg("review__rating"),total_rating = Sum("review__rating"))

    for f_an in filter_anno:
        print("---f_an--",f_an.avg_rating)
        print("---f_an--",f_an.total_rating)

    filter_anno = Rating.objects.filter(review = "ok").aggregate(avg_order_no = Avg("proxylearn__order_no"),total_order_no = Sum("proxylearn__order_no"))

    print("----filter_anno use ageg to relationship fields----",filter_anno)

    # the filter can be used after the annotate also possible
    # but it won't work for aggeregate functions

    filter_anno = ProxyLearn.objects.annotate(avg_rating = Avg("review__rating"),total_rating = Sum("review__rating")).filter(proxy_name="porur")

    for f_an in filter_anno:
        print("---filter after agg--",f_an.avg_rating)
        print("---ilter after agg--",f_an.total_rating)

    # we can have the dynamic filter in variale name then apply to the query set is possible

    highly_rated = Count("proxylearn", filter=Q(proxylearn__order_no__gte=7))
    rat = Rating.objects.annotate(num_books=Count("proxylearn"), highly_rated_books=highly_rated)

    for f_an in rat:
        print("---filter after agg--",f_an.num_books)
        print("---filter after agg--",f_an.highly_rated_books)
    
    # use filter inside the aggregation function is possible

    # but it was not adviceable #first use filter then use aggerigation is most efficient way 

    # if we want to filter first use the filter then use annotate or aggerigation is most efficient way to query

    filter_anno = Rating.objects.aggregate(avg_order_no = Avg("proxylearn__order_no",filter = Q(review = "ok")),total_order_no = Sum("proxylearn__order_no"))

    print("----filter_anno use ageg to relationship fields----",filter_anno)


    # view waht SQL query will executed during the orm process the query setqueryset


    filter_anno = Rating.objects.all()
    
    print("---query set query",str(filter_anno.query))

    # order_by in annotation

    filter_anno = ProxyLearn.objects.annotate(avg_rating = Avg("review__rating"),total_rating = Sum("review__rating")).filter(proxy_name="porur").order_by("avg_rating")

    # values in annotation which acts as a like GROUP BY 

    #GROUP BY

    # so the sum of value will be calculated but the grouping will be depends on the 'values' function fields 

    g_val = ProxyLearn.objects.values("proxy_name").annotate(sum_rating = Sum("review__rating"))

    print("----g_val----",g_val)
    
    for g in g_val:
        print(f"----g--{g.get('proxy_name')}----",g.get("count_rating"))
    
    # count

    g_val = ProxyLearn.objects.values("proxy_name").annotate(count_rating = Count("review__rating"))

    print("----count----",g_val)
    
    for g in g_val:
        print(f"----count--{g.get('proxy_name')}----",g.get("count_rating"))

    # values after annotate

    # the group by will not happend so use values first and then use annotate

    g_val = ProxyLearn.objects.annotate(sum_rating = Sum("review__rating")).values("proxy_name","sum_rating")

    print("----g_val--33333--",g_val)
    
    for g in g_val:
        print(f"--333--g--{g.get('proxy_name')}----",g.get("sum_rating"))

    # use annotate and aggregate in same query

    rat = Rating.objects.annotate(num_books=Count("proxylearn")).aggregate(Sum("num_books"))

    print("-------rat---------",rat)

    return HttpResponse("Aggerigation")

def learn_search(re):

    # SQL like %jj% filter

    search_result = SearchKey.objects.filter(search_keyword__icontains = "RUR")

    # search can be use only in postgresql and we have to mention the app in settings 

    # i.e django.contrib.postgres

    search_result = SearchKey.objects.filter(full_description__search = "RUR")

    # print("---search_result----.",search_result)

    for result in search_result:
        print("---search_keyword----.",result.search_keyword)

    # full text to search 

    # using search vector
    
    from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank,SearchHeadline

    # in this below query search vector is a method for full text to search 

    # and the args for searchvector is which field should be search

    # then filter search is what should be search

    # the result will be an array

    # it will return exact match only

    # and also if the text found any of one field it will return the resut

    # way 1 #it will returns all the field values like get_doc

    result = SearchKey.objects.annotate(search = SearchVector("search_keyword","rating__review",
                "proxy_learn__proxy_name")).filter(search="porur")
    
    print("---result--1--",result)

    for k in result:
        print("----------ss",k.rating)

    # way 2

    result = SearchKey.objects.annotate(search = SearchVector("search_keyword") + SearchVector("rating__review") 
                                        + SearchVector("proxy_learn__proxy_name")).filter(search="porur")
    
    print("---result--2--",result)


    # using SearchQuery

    # class SearchQuery(value, config=None, search_type='plain')

    # SearchQuery translates the terms the user provides into a search query object that the database compares to a 
    # search vector. By default, all the words the user provides are passed through the stemming algorithms, and then it 
    # looks for matches for all of the resulting terms.

    # sq1 and sq2 are same like it will search by porur then test

    # by default the search type is plain

    # When you create a SearchQuery object without specifying a model, it will search across all models that have a SearchVector field configured.

    sq1 = SearchQuery("porur test")

    vector =  SearchVector("search_keyword")

    result = SearchKey.objects.annotate(search = vector).filter(search = sq1)

    print("----sq-1--result--",result)

    sq2 = SearchQuery("test porur")

    result = SearchKey.objects.annotate(search = vector).filter(search = sq2)

    print("----sq-2--result--",result)

    # in this below it will search by 'test porur' together and sq3 and sq4 are the different query and result

    sq3 = SearchQuery("test porur",search_type="phrase") 

    result = SearchKey.objects.annotate(search = vector).filter(search = sq3)

    print("----sq-3--result--",result)   

    sq4 = SearchQuery("porur test",search_type="phrase")    

    result = SearchKey.objects.annotate(search = vector).filter(search = sq4)

    print("----sq-4--result--",result)

    # web search  #like logical operators

    sq5 = SearchQuery("'porur' ('test' OR 'nontest')  ",search_type="websearch") 

    result = SearchKey.objects.annotate(search = vector).filter(search = sq5)

    print("----sq-5--result--",result)

    # raw search

    sq6 = SearchQuery("'porur' & ('test' | 'nontest')  ",search_type="websearch")

    result = SearchKey.objects.annotate(search = vector).filter(search = sq6)

    print("----sq-6--result--",result)

    # these above search can be writtened most understable way like below

    sq12 = SearchQuery("porur") & SearchQuery("test")

    sq22 = SearchQuery("porur") | SearchQuery("test")

    result = SearchKey.objects.annotate(search = vector).filter(search = sq22)

    print("----sq-22--result--",result)

    sq32 = ~SearchQuery("porur") #not

    # learn about search rank

    # way 1

    rank1 = SearchRank(vector,sq22)

    result = SearchKey.objects.annotate(rank = rank1).order_by("-rank")

    print("-------rant 1---",result)

    for r in result:
        print(f"----rant ---{r.rank}--",r.search_keyword)

    # way 2 #both are same only

    rank2 = SearchRank("search_keyword","porur")

    result = SearchKey.objects.annotate(rank = rank2).order_by("-rank")

    print("-------rant 2---",result)

    for r in result:
        print(f"----rant ---{r.rank}--",r.search_keyword)

    # we filter the result by rank

    result = SearchKey.objects.annotate(rank = rank2).filter(rank__gte=0.001).order_by("-rank")

    print("-------rant 3---",result)

    for r in result:
        print(f"----rant ---{r.rank}--",r.search_keyword)

    # Learn about search headline
    # class SearchHeadline(expression, query, config=None, start_sel=None, stop_sel=None, max_words=None, min_words=None, short_word=None, highlight_all=None, max_fragments=None, fragment_delimiter=None)

    # Set the start_sel and stop_sel parameters to the string values to be used to wrap highlighted query terms in the document. PostgreSQL’s defaults are <b> and </b>.

    # Provide integer values to the max_words and min_words parameters to determine the longest and shortest headlines. PostgreSQL’s defaults are 35 and 15.

    # Provide an integer value to the short_word parameter to discard words of this length or less in each headline. PostgreSQL’s default is 3.

    # Set the highlight_all parameter to True to use the whole document in place of a fragment and ignore max_words, min_words, and short_word parameters. That’s disabled by default in PostgreSQL.

    # Provide a non-zero integer value to the max_fragments to set the maximum number of fragments to display. That’s disabled by default in PostgreSQL.

    # Set the fragment_delimiter string parameter to configure the delimiter between fragments. PostgreSQL’s default is

    # vectorh = SearchVector("search_keyword")

    search_query = SearchQuery("porur")
    
    head_result = SearchKey.objects.annotate(headline = SearchHeadline("search_keyword",search_query))

    print("--head_result--1--",head_result)

    for k in head_result:
        print("---h-r-q",k.search_keyword)
    
    head_result = SearchKey.objects.annotate(headline = SearchHeadline("search_keyword",search_query,start_sel="<span>",stop_sel="</span>"))

    # using different configurations

    head_result = SearchKey.objects.annotate(search = SearchVector("search_keyword",config="english")).filter(search = SearchQuery("porur",config="english"))

    # we can use fields also

    head_result = SearchKey.objects.annotate(search = SearchVector("search_keyword")).filter(search = SearchQuery(F("search_keyword")))

    # dynamic language

    # head_result = SearchKey.objects.annotate(search = SearchVector("search_keyword",config=F("language"))).filter(search = SearchQuery("porur",config=F("language")))

    # using weight in search is like raning 

    # The weight should be one of the following letters: D, C, B, A. By default, these weights refer to the numbers 0.1, 0.2, 0.4, and 1.0, respectively. If you wish to weight them differently, pass a list of four floats to SearchRank as weights in the same order above:


    sq1 = SearchQuery("porur")

    vector =  SearchVector("search_keyword",weight="A")

    rank2 = SearchRank(vector,sq1)

    result = SearchKey.objects.annotate(rank = rank2).order_by("-rank")

    rank2 = SearchRank("search_keyword","porur")

    result = SearchKey.objects.annotate(rank = rank2).order_by("-rank")

    vector =  SearchVector("search_keyword")

    rank2 = SearchRank(vector,sq1,weights=[0.2, 0.4, 0.6, 0.8])

    rank2 = SearchRank("search_keyword","porur",weights=[0.2, 0.4, 0.6, 0.8])

    result = SearchKey.objects.annotate(rank = rank2).order_by("-rank")

    # update search vector value

    # this is the way to update the vector if you want to use the search vector field to improve the search performance.

    val = SearchKey.objects.get(id=1)
    val.search_vector = "porur test"
    print("----val---",val.search_vector)
    val.save()

    re = SearchKey.objects.annotate(search = SearchVector("search_vector")).filter(search=SearchQuery("TEST"))

    print("---re---",re)

    # return render(re,"learning_orm_queries/index.html",{"search":re})

    # learn about trigram similarity

    learn_trigram()

    learn_accent_unaccent()

    return HttpResponse("Search")


def learn_trigram():
    # Trigram similarity
    # to use this first we have to activate the trigram in postgresql
    # by using the terminal command we can activate it
    # first looged into to postgrsql using user name like bench mariadb
    # then select database using the command \c django_learning
    # CREATE EXTENSION IF NOT EXISTS pg_trgm;
    # check if it is created or not
    # SELECT * FROM pg_extension WHERE extname = 'pg_trgm';

    # type 1

    # class TrigramSimilarity(expression, string, **extra)

    # Trigrams are sequences of three consecutive characters within a string. This approach is particularly useful for performing fuzzy text searching and similarity-based ranking in Django applications that use PostgreSQL as the database backend.

    # Benefits of Trigram Similarity:

    # Fuzzy Matching: It allows finding results that are similar but not necessarily identical to the search query, which is useful for handling typos and variations in user input.

    # Performance: Trigram indexes in PostgreSQL can significantly speed up text search queries, especially for large datasets, compared to traditional full-text search approaches.

    # Integration with Django: Django's integration with PostgreSQL's trigram features simplifies implementing advanced text search capabilities without requiring additional external libraries or tools.

    from django.contrib.postgres.search import TrigramSimilarity,TrigramDistance,TrigramWordSimilarity,TrigramStrictWordSimilarity

    re = SearchKey.objects.annotate(similarity = TrigramSimilarity("search_keyword","tes")).filter(similarity__gt=0.3).order_by("-similarity")

    print("---re--1---similarity----",re)


    # type 2

    # class TrigramWordSimilarity(string, expression, **extra)

    re = SearchKey.objects.annotate(similarity = TrigramWordSimilarity("tes","search_keyword")).filter(similarity__gt=0.3).order_by("-similarity")

    print("---re--2---similarity-word---",re)

    # difference betwwen the trigramsimilarity and trigramwordsimilarity is

    # both are is saving patterns like if we give 'india test' i will 

    # The trigram patterns for "india test" using TrigramSimilarity would be:

    # ind (from "india")
    # dia (from "india")
    # iat (from "india")
    # tes (from "test")
    # est (from "test")

    # TrigramWordSimilarity

    # The trigram patterns for "india test" using TrigramWordSimilarity would be:

    # ind (from "india")
    # dia (from "india")
    # tes (from "test")
    # est (from "test")

    # Use TrigramSimilarity when you want a more relaxed measure of similarity, allowing for minor variations in word forms or typos.
    # Use TrigramWordSimilarity when you want a more exact measure of similarity, requiring an exact match of the entire word.

    # exmaple i have two record one having 'test' another is 'porur test'

    # if we trying to search 'tes' in both types

    # the trigramsimilarity is giving one result which is 'test' record because which match 'tes'

    # but the trigramwordsimilarity is giving both the record 'test' and 'porur test' 

    re = SearchKey.objects.annotate(similarity = TrigramSimilarity("search_keyword","indian")).filter(similarity__gt=0.3).order_by("-similarity")

    print("---re--1---similarity-2---",re)
    
    
    re = SearchKey.objects.annotate(similarity = TrigramWordSimilarity("indian","search_keyword")).filter(similarity__gt=0.3).order_by("-similarity")

    print("---re--2---similarity-word--2-",re)

    # important example to  unserstand the TrigramWordSimilarity and rigramWordSimilarity

    # If you have a product called 'iPhone 14 Pro', both methods should return this product in the search results, 
    # since '14 pro' is a substring of the product name. However, the TrigramSimilarity method may also return other 
    # products with similar trigram patterns, such as 'iPhone 14 Pro Max' or 'iPhone 14 Pro Case', while the TrigramWordSimilarity 
    # method may return products with similar words, such as 'iPhone Pro' or '14 inch Laptop'.

    # TrigramStrictWordSimilarity

    # it is similar to TrigramWordSimilarity but match the exact trigram strictly TrigramStrictWordSimilarity

    re = SearchKey.objects.annotate(similarity = TrigramStrictWordSimilarity("indian","search_keyword")).filter(similarity__gt=0.3).order_by("-similarity")

    print("---re--3---similarity-word--3-",re)

    # -----------------TrigramDistance---------------

    # class TrigramDistance(expression, string, **extra)

    # Identify Trigrams: First, the algorithm extracts all possible trigrams from both strings. For example, the trigrams of the string "apple" would be "app", "ppl", "ple".

    # Compare Trigrams: It then counts how many trigrams are common between the two strings. The more trigrams they share, the more similar the strings are considered to be.

    # Calculate Distance: Trigram distance is often calculated as the complement of the number of shared trigrams divided by the total number of distinct trigrams present in both strings. Alternatively, it can also be represented as a similarity measure, where the distance is the ratio of shared trigrams to the total number of distinct trigrams.

    # Trigram distance can be useful in various applications such as spell checking, plagiarism detection, and string matching, where it helps determine how closely two strings resemble each other based on their character sequences. It’s a simple yet effective way to gauge similarity in terms of character sequence overlap.

    re = SearchKey.objects.annotate(distance = TrigramDistance("search_keyword","indian")).filter(distance__lte=0.3).order_by("-distance")

    print("---re--1---trigram--distance--1-",re)

    # TrigramWordDistance¶ -------------------2

    # class TrigramWordDistance(string, expression, **extra)

    # TrigramStrictWordDistance¶ ----------------3

    # class TrigramStrictWordDistance(string, expression, **extra)


    # default functions in postgresql-----------------

    # 1 trigram_similar

    trigr = SearchKey.objects.filter(search_keyword__trigram_similar="test")

    print("--trigr--1-",trigr)

    # 2 trigram_word_similar

    trigr = SearchKey.objects.filter(search_keyword__trigram_word_similar="test")

    print("--trigr--2-",trigr)

    # 3 trigram_strict_word_similar

    tr = SearchKey.objects.filter(search_keyword__trigram_strict_word_similar="test")

    print("--trigr--3-",tr)


def learn_accent_unaccent():
    # Here are some common examples of accents and diacritical marks:

    # Acute Accent (´): A mark placed above a vowel to indicate stress or sometimes a change in pronunciation. For example, in Spanish, "á" is pronounced differently from "a".

    # SELECT * FROM persons 
    # WHERE f_unaccent(name) ILIKE f_unaccent('%Jose%')

    # ---------add extension in db level

    # CREATE EXTENSION IF NOT EXISTS unaccent;

    # The unaccent lookup can be used on CharField and TextField:

    # unac = SearchKey.objects.filter(search_keyword__unaccent="test")

    pass

    # print("----unaccent--1",unac)

def learn_database_functions(re):

    result = []



    return render(re,"learning_orm_queries/index.html",{"db_fun":result})


def learn_query_expressions(re):

    result = []

    from django.db.models.functions import Upper,Length

    # exp - 1

    # -------------------using F

    from django.db.models import F,Value

    result = QueryExps.objects.filter(age__gt = F("nos"))

    result = QueryExps.objects.filter(age__gt = F("nos") * 0)

    result =[ QueryExps.objects.filter(age__gt = F("nos") * 0).first()  ] 

    # so the F function , how it will use in real case and improve the performance like below

    # if you want to increase the age of each record means how could you do normally like below

    result = QueryExps.objects.all()

    for k in result:
        d = QueryExps.objects.get(pk=k.id)
        d.age = d.age + 1
        d.save()

    # the above method is not correct , which mean if we have bulkk records it direct case to performance issue

    # intead of doing this the optimized way is #you cann understand the difference

    result = QueryExps.objects.update(age = F("age") + 1)

    # -------------avoid

    # reporter = Reporters.objects.get(name="Tintin")
    # reporter.stories_filed = F("stories_filed") + 1
    # reporter.save()

    # reporter.name = "Tintin Jr."
    # reporter.save()

    # stories_filed will be updated twice in this case. If it’s initially 1, the final value will be 3. This persistence can be avoided by reloading the model object after saving it, for example, by using refresh_from_db().

    # --using for create dynamic value

    result = QueryExps.objects.annotate(age_no_diff = F("age") - F("nos"))

    # ---------using Floatfield and Decimalfield during above dynamic operation may be error because the python
    # confuesed too gove result weather in Fload field or Decimalfield so we have to use the output field

    from django.db.models import ExpressionWrapper,FloatField

    result = QueryExps.objects.annotate(age_no_diff = ExpressionWrapper( F("age") - F("nos"),output_field=FloatField())  )

    #---------------null first and null last in order by
   
    result = QueryExps.objects.order_by(F("name").desc(nulls_first = True))
    result = QueryExps.objects.order_by(F("name").desc(nulls_last = True))
   
    # ----------invert the boolen field dynamically 
    
    # for example if we have check box we have to update it like if it is true have to make false 

    # if it is false have to make it true like we can use like below

    result = QueryExps.objects.update(verified = ~F("verified"))

   
    #---------------------- Upper

    result = QueryExps.objects.annotate(exe_f = Upper(F("name")))

    # giving static value in upper case to save in db

    result = QueryExps.objects.annotate(exe_f = Upper(Value("name")))
    
    # ------------------Length

    # way 1

    result = QueryExps.objects.order_by(Length("name").asc())

    result = QueryExps.objects.order_by(Length("name").desc())

    # way 2 #register the lookup and then use directly like custom lookup

    from django.db.models import CharField

    CharField.register_lookup(Length)

    result = QueryExps.objects.order_by("-name__length")

    #-------------------------------- Exists

    from django.db.models import Exists,OuterRef

    # way 1

    # outref is used to refer outer query field values

    result = QueryExps.objects.filter(Exists(QueryExps.objects.filter(age__lt = 100),age__gt = 0))

    result = QueryExps.objects.filter(Exists(QueryExps.objects.filter(age__lt = OuterRef("age")),age__gt = 0))

    # --------------------------GreaterThan

    from django.db.models.lookups import GreaterThan

    result = QueryExps.objects.filter(GreaterThan(F("age"),0))


    return render(re,"learning_orm_queries/index.html",{"q_exp":result})
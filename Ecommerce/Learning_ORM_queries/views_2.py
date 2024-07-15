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

    # ****************** ref document

    # by default the RelatedManager used for reverse relations is a subclass of the default manager for that model. If you would like to specify a different manager for a given query you can use the following syntax:
    
    # b.entry_set(manager="entries").all()

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


def learn_query_expressions(re):

    result = []

    from django.db.models.functions import Upper,Length,Lower

    # exp - 1

    # -------------------using F

    from django.db.models import F,Value

    result = QueryExps.objects.filter(age__gt = F("nos"))

    result = QueryExps.objects.filter(age__gt = F("nos") * 0)

    result =[ QueryExps.objects.filter(age__gt = F("nos") * 0).first()  ] 

    # so the F function , how it will use in real case and improve the performance like below

    # if you want to increase the age of each record means how could you do normally like below

    # result = QueryExps.objects.all()

    # for k in result:
    #     d = QueryExps.objects.get(pk=k.id)
    #     d.age = d.age + 1
    #     d.save()

    # the above method is not correct , which mean if we have bulkk records it direct case to performance issue

    # intead of doing this the optimized way is #you cann understand the difference

    # result = QueryExps.objects.update(age = F("age") + 1)

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

    # result = QueryExps.objects.update(verified = ~F("verified"))

   
    #---------------------- Upper

    result = QueryExps.objects.annotate(exe_f = Upper(F("name")))

    # giving static value in upper case to save in db

    result = QueryExps.objects.annotate(exe_f = Upper(Value("abcd")))
    
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

    #---------------------- Func() expressions

    from django.db.models import Func

    # both are the same functionality

    result = QueryExps.objects.annotate(exe_f = Func(F("name"), function = "Lower"))

    result = QueryExps.objects.annotate(exe_f = Lower(F("name")))

    print("---------------***result----",result)

    result = learn_condition_expression()

     #------------------- use Subquery 

    # class Subquery(queryset, output_field=None)

    from django.db.models import Subquery

    # subquery is like real sql subquery only

    # this is not subquery but short way to use like subquery

    result = QueryExps.objects.filter(name = QueryExps.objects.filter(name="Dinesh")[0].name)

    # subquery

    result = QueryExps.objects.filter(name = Subquery(QueryExps.objects.filter(name__icontains="sh").values_list("name")[:1]))

    # -------------------- class OuterRef(field)

    from django.db.models import OuterRef

    # --here get won't work

    # result = QueryExps.objects.filter(name = Subquery(QueryExps.objects.get(pk = OuterRef("pk"))))

    # below --filter is correct query---

    subquery = QueryExps.objects.filter(pk=OuterRef("pk")).values('name')
    result = QueryExps.objects.filter(name=Subquery(subquery))

    # -----using with filer,values,calues_list

    # >>> from django.db.models import OuterRef, Subquery, Sum
    # >>> comments = Comment.objects.filter(post=OuterRef("pk")).order_by().values("post")
    # >>> total_comments = comments.annotate(total=Sum("length")).values("total")
    # >>> Post.objects.filter(length__gt=Subquery(total_comments))

    # ---raw vs rawsql

    # ---raw like django model instance queryset only but we can write sql condition

    # The raw method in Django is used to execute raw SQL queries and return model instances. It allows you to write custom SQL queries and map the results directly to Django model instances. 

    # : It returns a RawQuerySet instance, which behaves like a normal QuerySet but represents raw query results as model instances.
    # The columns selected in the raw SQL query must correspond to fields in the Django model. Django uses the model's _meta information to map columns to model fields.
    
    # for postgresql the table name shout be in -----""----double quote like below otherwise it shows does not exists erroor

    result = QueryExps.objects.raw("""SELECT * FROM "Learning_ORM_queries_queryexps" """)

    print("--------result--raw---------",result)

    for r in result:
        print("---r-----",r.name)

 
    # ---rawsql -- pure sql --directly from database not django queryset

    # class RawSQL(sql, params, output_field=None)

    from django.db.models.expressions import RawSQL

    # params is mandatory to give it in the function

    result = QueryExps.objects.annotate(exe_f = RawSQL(' SELECT name FROM "Learning_ORM_queries_queryexps" LIMIT 1',params = ["s"]))

    result = QueryExps.objects.annotate(exe_f = RawSQL(' SELECT name FROM "Learning_ORM_queries_queryexps" WHERE name = %s ',params = ["Dinesh"]))

    # ----window functions
   
    #class Window(expression, partition_by=None, order_by=None, frame=None, output_field=None)

    # we can use aggerigate function to aggerigate the values but the problem is it will aggerigate all the rows

    # but when use the window function we can define the partition like group by  but not exactly group by 

    # to understand this see the exp below
   
    from django.db.models import Sum,Window,Avg,Min,Q

    # in this example what is done means the sum of age is calculated only for the 'age' and 'name' fields values are same accross the all records


    result = QueryExps.objects.annotate(exe_f = Window(
                                expression = Sum("age"),
                                partition_by = [F("age"),F("name")],
                                order_by = "age"
    ))
    
    # --multiple window use case

    window = {
         "partition_by":[F("age"),F("name")],
          "order_by":"age"
    }

    result = QueryExps.objects.annotate(exe_f = Window(
                                            expression = Sum("age"),
                                            partition_by = [F("age"),F("name")],
                                            order_by = "age"),
                                exe_f_1 = Window(
                                    expression = Avg("age"),
                                    partition_by = [F("age"),F("name")],
                                    order_by = "age"
                                                    ),
                                exe_f_2 = Window(
                                    expression = Min("age"),**window)
                                    
                                    )
   
    # Rules
    

    result = QueryExps.objects.annotate(exe_f = Window(
                                expression = Sum("age"),
                                partition_by = [F("age"),F("name")],
                                order_by = "age"
    )).filter(exe_f__gt = 10)

    result = QueryExps.objects.annotate(exe_f = Window(
                                expression = Sum("age"),
                                partition_by = [F("age"),F("name")],
                                order_by = "age"
    )).filter(Q(exe_f__gt = 10) | Q(name="Gopi"))

    # query = """
    #     SELECT *,
    #            SUM(age) OVER (PARTITION BY age, name ORDER BY age ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS exe_f
    #     FROM your_table_name
    #     WHERE exe_f > 10 OR name = 'Gopi'
    # """

    # he reason for this limitation is that window functions are evaluated after the WHERE clause, so the database 
    # can't use the window function results in the WHERE clause. This makes it difficult to implement filtering on 
    # window functions with disjunctive predicates.

    # >>> qs = Movie.objects.annotate(
    # ...     category_rank=Window(Rank(), partition_by="category", order_by="-rating"),
    # ...     scenes_count=Count("actors"),
    # ... ).filter(Q(category_rank__lte=3) | Q(title__contains="Batman"))
    
    from django.db.models import RowRange,ValueRange

    # ---------RowRange

    result = QueryExps.objects.annotate(exe_f = Window(
                                expression = Sum("age"),
                                partition_by = [F("age"),F("name")],
                                order_by = "age",
                                frame=RowRange(start=-3,end=0)
    )).filter(Q(exe_f__gt = 10) | Q(name="Gopi"))

    # in this above examples

    # if i have 5 records matching the partitiob means i.e group it will looking before 3 rows values and current row value to sum
    # for examples if i have 5 rows having values 1000 on each,matching values
    # my current row is 1st row so the result will be 1000 because of there is no previous rows avaiable 
    # my current row is 2nd row so the result will be 2000 because of there is 1 row avaiable and current row
    # i have menthond "start=-3" and "end=0" so on each row while SUM happening the SUM will include 
    # current row and previous 3 rows only 
    # start=-3 means previous 3 rows not current row included
    # end=0 means include current row 

    result = QueryExps.objects.annotate(exe_f = Window(
                                expression = Sum("age"),
                                partition_by = [F("verified")],
                                order_by = "name",
                                frame=RowRange(start=-3,end=0)
    )).order_by("pk")

    # -----class ValueRange(start=None, end=None)


    # result = QueryExps.objects.annotate(exe_f = Window(
    #                             expression = Sum("age"),
    #                             partition_by = [F("verified")],
    #                             order_by = "name",
    #                             frame=ValueRange(start=-12,end=12)
    # )).order_by("pk")

    # If a movie’s “peers” are described as movies released by the same studio in the same genre in the same year, this RowRange example annotates each movie with the average rating of a movie’s two prior and two following peers:

    # >>> from django.db.models import Avg, F, RowRange, Window
    # >>> Movie.objects.annotate(
    # ...     avg_rating=Window(
    # ...         expression=Avg("rating"),
    # ...         partition_by=[F("studio"), F("genre")],
    # ...         order_by="released__year",
    # ...         frame=RowRange(start=-2, end=2),
    # ...     ),
    # ... )

    # If the database supports it, you can specify the start and end points based on values of an expression in the partition. If the released field of the Movie model stores the release month of each movie, this ValueRange example annotates each movie with the average rating of a movie’s peers released between twelve months before and twelve months after each movie:

    # >>> from django.db.models import Avg, F, ValueRange, Window
    # >>> Movie.objects.annotate(
    # ...     avg_rating=Window(
    # ...         expression=Avg("rating"),
    # ...         partition_by=[F("studio"), F("genre")],
    # ...         order_by="released__year",
    # ...         frame=ValueRange(start=-12, end=12),
    # ...     ),
    # ... )



    return render(re,"learning_orm_queries/index.html",{"q_exp":result})

# --------------------------------------------------

def learn_condition_expression():
    # ---using when case then default output field
    
    from django.db.models import When,Value,Case,CharField

    result = []

    result = QueryExps.objects.annotate(exe_f = Case(When(name__icontains = "sh",then=Value("dines")),
                                         When(age__gt = 50,then = F("description")),
                                         default=Value("poda"),
                                         output_field = CharField()
                                          ))

    result = QueryExps.objects.annotate(exe_f = Case(When(name__icontains = "sh",then=Value("dines")),
                                         When(age__gt = 50,then = F("description")),
                                         default=Value("poda"),
                                         output_field = CharField()
                                          )).filter(exe_f__isnull=False)

    # values vs values list

    # values are key values pairs and which initiate the model instance to get the field name

    # values_list are tuple of values there is no need to initiate the model instance

    # when dealing with large data sets and performance needed the valuelist is perform better

    # when needed key value pair list the values is better

    
    result = QueryExps.objects.annotate(exe_f = Case(When(name__icontains = "sh",then=Value("dines")),
                                         When(age__gt = 50,then = F("description")),
                                         default=Value("poda"),
                                         output_field = CharField()
                                          )).filter(exe_f__isnull=False).values_list()


    result = QueryExps.objects.annotate(exe_f = Case(When(name__icontains = "sh",then=Value("dines")),
                                         When(age__gt = 50,then = F("description")),
                                         default=Value("poda"),
                                         output_field = CharField()
                                          )).filter(exe_f__isnull=False).values()
    
    # -----when case not only with annotate and can be usd with filter also


    result = QueryExps.objects.filter(name__icontains = Case(
                                                            When(age__gt=50,then=F("name")),
                                                            default = Value("poda"),
                                                            output_field = CharField())
                                                            ).values()
    
    # -----use conditional expression in update

    # from django.db.models import IntegerField
    
    # result = QueryExps.objects.update(age = Case(When(name__icontains = "nesh",then=Value(1)),default = Value(1000),output_field=IntegerField()))

    # result = [QueryExps.objects.get(pk=result)]

    print("------------re---",result)


    return result
    

def learn_expression_api(request):
    result = []

    from django.db.models import Sum

    result = ExpLearn1.objects.all()

    return render(request,"learning_orm_queries/index.html",{"lea_exp":result})



def learn_database_functions(re):
    
    result = []

    #------Cast function

    # class Cast(expression, output_field)

    from django.db.models.functions import Cast
    from django.db.models import FloatField


    result = ExpLearn1.objects.annotate(exe_f = Cast(F("age"),output_field=FloatField()))

    # ------ class Coalesce(*expressions, **extra)

    # if we have two fields with similar datatype and want to fetch not null values by which is first list mentioned in coalesce

    # like below if description having value it will be fetched if decription is null then name fetched

    from django.db.models.functions import Coalesce

    result = ExpLearn1.objects.annotate(exe_f = Coalesce("description","name"))

    # what happedn when two or many of the fields having null values like below

    # no error throw and none value will be returned

    result = ExpLearn1.objects.annotate(exe_f = Coalesce("description","title"))

    # if all fields having null means we can set a statisc value like below

    esult = ExpLearn1.objects.annotate(exe_f = Coalesce("description","title",Value("ss")))

    # Prevent an aggregate Sum() from returning None

    from django.db.models import Sum

    result = ExpLearn1.objects.annotate(exe_f = Coalesce(Sum("age"),0))

    # --------------- class Collate(expression, collation)

    # collate means it will ignore the databse case sensitiity 

    # if i have a value in db like 'gopi' or 'Gopi' and the db is case sensitivity means we have give exact value like mentioned

    # but when using like below it will filter both the values rows

    # from django.db.models.functions import Collate

    # result = ExpLearn1.objects.filter(name = Collate(Value("GOPI"),"nocase"))

    # ----------- class Greatest(*expressions, **extra)

    # the two or more comparsion fields must be same datatype

    # if the two fields having null means the null will be returned

    from django.db.models.functions import Greatest

    result = ExpLearn1.objects.annotate(exe_f = Greatest("creation","modified"))

    # handle null values and return default value

    import datetime

    from django.db.models.fields import DateTimeField

    # here is the creation and modified null means the grestest value in default one so the default one will be return but this is not recommended way

    result = ExpLearn1.objects.annotate(exe_f = Greatest("creation","modified",Value(datetime.datetime.now()),output_field=DateTimeField()))

    # right way

    result = ExpLearn1.objects.annotate(exe_f = Coalesce( Greatest("creation","modified"),Value(datetime.datetime.now()),output_field=DateTimeField()))

    #---------------------class JSONObject(**fields)

    # it will annottate a json in a single key to all the rows

    from django.db.models.functions import JSONObject,Lower

    result = ExpLearn1.objects.annotate(exe_f = JSONObject(name = "name",des = Lower("description"),age = F("age") + 1))


    # ----------------class Least(*expressions, **extra)

    from django.db.models.functions import Least

    result = ExpLearn1.objects.annotate(exe_f = Least("creation","modified"))

    # ------------class NullIf(expression1, expression2)

    from django.db.models.functions import NullIf

    # use case it get two or more field names and check weather all the fields are 'equal' if not then the first field value will be return

    #if all field values equal then it will return 'null'

    result = ExpLearn1.objects.annotate(exe_f = NullIf("creation","modified"))

    return render(re,"learning_orm_queries/index.html",{"db_fun":result})

def learn_datetime_database_functions(request):

    result = []

    result = LearnDateDbFunc.objects.all()

    #  class Extract(expression, lookup_name=None, tzinfo=None, **extra)¶

    # similar like below we can use hour,second,minute,week_day

    result = LearnDateDbFunc.objects.filter(start_datetime__year = "2024")

    result = LearnDateDbFunc.objects.filter(start_datetime__iso_year = "2024")

    result = LearnDateDbFunc.objects.filter(start_datetime__quarter = 2)

    result = LearnDateDbFunc.objects.filter(start_datetime__month = 6)

    # filter itself working fine but how we can extracrt like year,day,month from a datetime,date field

    from django.db.models.functions import Extract,ExtractDay,ExtractHour,ExtractMinute,ExtractMonth

    result = LearnDateDbFunc.objects.filter(start_datetime__month= Extract("start_datetime","month"))

    result = LearnDateDbFunc.objects.filter(start_datetime__month= ExtractMonth("start_datetime"))

    # for querying purpose

    result = LearnDateDbFunc.objects.annotate(exe_f = ExtractHour("start_datetime"))

    # using different time zones

    import zoneinfo
    
    melb = zoneinfo.ZoneInfo("Australia/Melbourne")

    result = LearnDateDbFunc.objects.annotate(exe_f = ExtractHour("start_datetime",tzinfo=melb))

    # -------- now function

    from django.db.models.functions import Now

    from django.db.models import DateTimeField,DateField


    result = LearnDateDbFunc.objects.filter(start_datetime__lt=Now())

    # --------------class Trunc(expression, kind, output_field=None, tzinfo=None, **extra)

    from django.db.models.functions import Trunc

    from django.db.models import Count

    result = LearnDateDbFunc.objects.annotate(exe_f = Trunc("start_datetime",kind="day",output_field=DateTimeField())
                                              ).values("exe_f").annotate(name = Count("id"))

    # explanation

    # in this below and above query exp the Trunc function is takes datetime field values

    # and convert it into day means '22' and below in year means '2024'

    # and match the values to all the records in db 

    # the comparsion will be the 'start_datetime' having value of date and time but the comparsion is by 

    # only date for above then below is year not datetime value comparsion


    from django.db.models import IntegerField

    result = LearnDateDbFunc.objects.annotate(exe_f = Trunc("start_datetime",kind="year",output_field=DateTimeField())
                                              ).values("exe_f").annotate(name = Count("id"))

    result = LearnDateDbFunc.objects.annotate(exe_f = Trunc("start_datetime",kind="year",output_field=DateTimeField())
                                              ).values("exe_f")
    
    for r in result:
        print("------------r",r)

    result = LearnDateDbFunc.objects.annotate(exe_f = Trunc("start_datetime",kind="year",output_field=DateTimeField())
                                              )
    
    # similar to extract and also we can add timezone like extract ref extract

    from django.db.models.functions import TruncDate,TruncDay,TruncHour,TruncMinute

    result = LearnDateDbFunc.objects.annotate(exe_f = TruncDate("start_datetime"))

    return render(request,"learning_orm_queries/index.html",{"db_date_fun":result})

def learn_math_db_functions(request):

    # thers is bunch of functions here for understanding inly dew fucntion used here 
    # more functions like reverse,replace are avaiable , check the document

    result = []

    result = DbMathFunc.objects.all()

    # 1 ------- Abs
    # class Abs(expression, **extra)

    from django.db.models.functions import Abs

    from django.db.models import FloatField,IntegerField

    FloatField.register_lookup(Abs)

    IntegerField.register_lookup(Abs)


    result = DbMathFunc.objects.annotate(exe_f = Abs("int_value"))

    # here the negative int value first converted into positive then the value 0 wille be compared to the positive value

    result = DbMathFunc.objects.filter(int_value__abs__gt = 0)

    #2---------class Ceil(expression, **extra)

    from django.db.models.functions import Ceil


    FloatField.register_lookup(Ceil)

    IntegerField.register_lookup(Ceil)


    result = DbMathFunc.objects.annotate(exe_f = Ceil("float_value"))

    result = DbMathFunc.objects.filter(float_value__ceil__gt = 0)


    #3---------lass Floor(expression, **extra)

    from django.db.models.functions import Floor


    FloatField.register_lookup(Floor)

    IntegerField.register_lookup(Floor)


    result = DbMathFunc.objects.annotate(exe_f = Floor("float_value"))

    result = DbMathFunc.objects.filter(float_value__floor__gt = 0)


    #4--------------class Mod(expression1, expression2, **extra)
    # modulo like in python 5%2

    from django.db.models.functions import Mod


    result = DbMathFunc.objects.annotate(exe_f = Mod("int_value","float_value"))

    # $5---------------- lass Power(expression1, expression2, **extra)

    from django.db.models.functions import Power


    result = DbMathFunc.objects.annotate(exe_f = Power("int_value","floor_no"))  

   
    # 6--------------------class Random(**extra)

    # Returns a random value in the range 0.0 ≤ x < 1.0.

    from django.db.models.functions import Random


    result = DbMathFunc.objects.annotate(exe_f = Random())  


    # 7--------------------class Round(**extra)

    # By default, it rounds to the nearest integer. 
    
    from django.db.models.functions import Round


    result = DbMathFunc.objects.annotate(exe_f = Round("float_value"))

    result = DbMathFunc.objects.annotate(exe_f = Round("float_value", precision = 2))  

    # 8-------------class Sqrt(expression, **extra)

    from django.db.models.functions import Sqrt

    print('--------------------------------------------------------------------',chr(98))

    result = DbMathFunc.objects.filter(floor_no=2).annotate(exe_f = Sqrt("floor_no"))

    # 9--------------------------------class Chr(expression, **extra)

    from django.db.models.functions import Chr

    result = DbMathFunc.objects.filter(floor_no=2).annotate(exe_f = Chr(Value(98)))

    # 10--------------------------------class Concat(*expressions, **extra

    from django.db.models.functions import Concat

    result = DbMathFunc.objects.annotate(exe_f = Concat(Value("floor_no"),Value("int_value")))

   
    #11------------------------class Left(expression, length, **extra)

    # like slicing but the index will from 1 so if 2 means the first two values will be return

    from django.db.models.functions import Left,Length,Lower

    result = DbMathFunc.objects.annotate(exe_f = Left("description",length=2))

    #12--------------class Length(expression, **extra)

    # returns the length of the string

    result = DbMathFunc.objects.annotate(exe_f = Length("description"))


    result = DbMathFunc.objects.annotate(exe_f = Lower("description"))

    #13----------------------SHA1, SHA224, SHA256, SHA384, and SHA512

    # we need to install the pgcrypto extension on ##POSTGRESQL to perfom the hasing

    # the above classes are different type hasing classes to hash the string

    from django.db.models.functions import SHA1,SHA224,SHA256,SHA384,SHA512

    result = DbMathFunc.objects.annotate(exe_f = SHA1("title"))

    # 14-----------------------------lass StrIndex(string, substring, **extra)

    from django.db.models.functions import StrIndex

    # here we having the #Value as second argument as s

    # do if the title field having 's' value means it will return the index

    # important index is started from 1 not 0 like list

    result = DbMathFunc.objects.annotate(exe_f = StrIndex("title",Value("s")))

    # 15----------------------class Substr(expression, pos, length=None, **extra)

    from django.db.models.functions import Substr

    # it is used to slicing i.e index starting from 1

    # here the title having value 'test' i gave the pos is 4 so the value return in the field is 't'

    result = DbMathFunc.objects.annotate(exe_f = Substr("title",pos=4))

    # here the 3rd args is '1' mention like after the '2' character hoe many character needs to be return

    # so here title having 'test' and the start is 2 and length is 1 so the value will be 'e' only


    result = DbMathFunc.objects.annotate(exe_f = Substr("title",2,1))

    # if i give 2 it will return 'es'
    
    result = DbMathFunc.objects.annotate(exe_f = Substr("title",2,2))

    # 16----------------class Trim(expression, **extra)

    # trim is like python trim it will remove spaces form string

    from django.db.models.functions import Trim

    result = DbMathFunc.objects.annotate(exe_f = Trim("title"))


    return render(request,"learning_orm_queries/index.html",{"db_math_fun":result})



def learn_window_db_functions(request):

    # refer the document 

    # the functions are not much needed

    # RowNumber.\,Rank,PercentRank,Ntile,NthValue,Lead¶,LastValue,Lag,FirstValue,DenseRank,CumeDist

    result = []

    result = DbMathFunc.objects.all()

    return render(request,"learning_orm_queries/index.html",{"db_math_fun":result})


def learn_custom_managers(request):

    # refer the document 

    # the functions are not much needed

    # RowNumber.\,Rank,PercentRank,Ntile,NthValue,Lead¶,LastValue,Lag,FirstValue,DenseRank,CumeDist

    result = []

    result = LearnManager.my_manager.all()

    # A custom Manager method can return anything you want. It doesn’t have to return a QuerySet.

    # Another thing to note is that Manager methods can access self.model to get the model class to which they’re attached.

    result = LearnManager.cust_manager_1.get_title_value() #this is the custom manager method

    # result = LearnManager.objects.all()
    
    # accessing related objects 

    # By default, Django uses an instance of the Model._base_manager manager class when accessing related objects 
    # (i.e. choice.question), not the _default_manager on the related object. #the default manager is 'objects'

    result = ManagerDetail.objects.all() #it apply the manager fileter and fetch the data

    result = LearnManager.my_manager.all()

    for re in result:
        print("---re",re.manager_detail)

    # result = [LearnManager.my_manager.get(pk=1)]


    # for re in result:
    #     print("---basemanager----------",re.manager_detail)

    # 2------------------custom queryset 

    # here the high_rated is custom queryset see models.py to more details

    result = LearnManager.cust_manager_1.hight_rated()

    # 3----------manager with queryset

    # this is the public method so that can beaccessed by both queryset and custom manager like below

    result = LearnManager.cust_manager_2.hight_rated()

    result = CustomManager2_WithQueryset(LearnManager).hight_rated()


    # trying to access private method

    # in this case the manage can't be access the private method like below first method

    # result = LearnManager.cust_manager_2._low_rated()

    result = CustomManager2_WithQueryset(LearnManager)._low_rated()

    # the method _most_valuable is set to queryset_only is fasle so we can access the method by manager even it private method

    result = LearnManager.cust_manager_2._most_valuable()

    result = CustomManager2_WithQueryset(LearnManager)._most_valuable()

    # 4--------------------classmethod from_queryset(queryset_class)

    result = LearnManager.cust_manager_3.hight_rated()

    # 5--------------using inherited model to test parent manager

    result = ChildLearnManager.my_manager.all()

    result = ChildLearnManager.cust_manager_3.hight_rated()

    result = ChildLearnManager.child_manager.all()

    return render(request,"learning_orm_queries/index.html",{"manager_fun":result})

from django.db import transaction
# transaction.atomic(using=None, savepoint=True, durable=False)#using is the name of the database
# @transaction.non_atomic_requests #the decorator which is used to disble the atomic transaction nature to the particular request , which is used when we use atomic_request = true enables in settings.py ,which mean all the http request will be atomic requests.
# @transaction.atomic #if the decorator is used even the auto commit enbles the trasaction wont be auto commited which means below the two queries eill be rollback if any error rises
def learn_database_transactions(request):

    result = []

    #1-------------- by default the django usess auto commit for each transaction

    # query1 = DBTransactions()
    # query1.title = "trans 3"
    # query1.description = "descript 3"
    # query1.rating = 3
    # query1.save()


    # query2 = DBTransactions()
    # query2.title = "trans 4wsrfsas" #here title is max chr is 10 but i gave more than 10
    # query2.description = "descript 4"
    # query2.rating = "4" 
    # query2.save()

    # In the above example, each query is executed in its own transaction. If Query 2 fails, the database will roll back 
    # only Query 2, and the changes made by Query 1 (creating the user) will be committed.

    # 2------------------- atomic request = true in settings.py so every query in the view is consider as a single query
    # so the one of the query failes all the query transaction will be rollback
    # in the above the query1 is one transaction and autocommited and another is separate so the one query executed and
    # auto commited to db so one recired will be avaioable to overcome this below func example is used

    # i have enbled the atomic request = True in settings.py but still the first query will br commited to the database
    # because the ORM having auto commit = True so the first query won't be rollback evan atomic enables
    # the second query having errors

    query1 = DBTransactions()
    query1.title = "trans 5"
    query1.description = "descript 5"
    query1.rating = 5
    query1.save()


    query2 = DBTransactions()
    query2.title = "trans 6wsrfsas" #here title is max chr is 10 but i gave more than 10
    query2.description = "descript 6"
    query2.rating = "6" 
    query2.save()

    # To overcome the above scnario the below method is used    

    # learn_database_transac_1()

    # the another method to rollback the trnsactions

    learn_database_transac_2()

    return render(request,"learning_orm_queries/index.html",{"db_trans":result})

def learn_database_transac_1():
    from django.db import transaction

    # here we have two transaction but when we use transaction.atomic it will be consider as a single transaction

    # so if any one of these failes the two transactions will be rollbacked

    with transaction.atomic():

        query1 = DBTransactions()
        query1.title = "trans 7"
        query1.description = "descript 7"
        query1.rating = 7
        query1.save()


        query2 = DBTransactions()
        query2.title = "trans 6wsrfsas" #here title is max chr is 10 but i gave more than 10
        query2.description = "descript 8"
        query2.rating = "8" 
        query2.save()

    # In order to guarantee atomicity, atomic disables some APIs. Attempting to commit, roll back, or change the 
    # autocommit state of the database connection within an atomic block will raise an exception


def learn_database_transac_2():
    from django.db import transaction

    # so if any one of these failes the two transactions will be rollbacked

    # this is not correct method,by default the transaction will be rollback
    # but some case it will be useful

    try:
        query2 = DBTransactions()
        query2.title = "trans 6wsrfsas" #here title is max chr is 10 but i gave more than 10
        query2.description = "descript 10"
        query2.rating = "10" 
        query2.save()
    except ValidationError:
        transaction.set_rollback(True)
        raise

def learn_auto_commit(request):

    result = []

    # #################33 in the settings.py the auto commit is set to false sono commit happend

    # In the SQL standards, each SQL query starts a transaction, unless one is already active. 
    # Such transactions must then be explicitly committed or rolled back

    # from django.db import transaction

    # # Disable auto-commit
    # transaction.set_autocommit(False)

    # try:
    #     # Your database operations here
    #     transaction.commit()  # Commit the transaction
    # except:
    #     transaction.rollback()  # Rollback the transaction if an error occurs
    # finally:
    #     transaction.set_autocommit(True)  # Restore auto-commit behavior

    # 1-------------autp commit is false in the setting.py

    # here the two transaction will be rollback if error rise and two transaction will be commited when use commit only
    # other wise the record not commited to databse.

    from django.db import transaction

    try:
        query1 = DBTransactions()
        query1.title = "trans 11"
        query1.description = "descript 11"
        query1.rating = 11
        query1.save()


        query2 = DBTransactions()
        query2.title = "trans 6wsrfsas" #here title is max chr is 10 but i gave more than 10
        query2.description = "descript 11"
        query2.rating = "11" 
        query2.save()

        transaction.commit()

    except Exception:
        transaction.rollback()
    
    # 2 #--------------- after the record saved some times we  have to do some actions like email sending for that below function used

    # this is the manual transaction beecause of auto commit is fales in settings

    # However, when you're using manual transaction management (i.e., you've disabled autocommit and are managing t
    # ransactions explicitly using transaction.set_autocommit(False) or @transaction.atomic), you can't use on_commit().
    
    # The reason is that on_commit() relies on Django's automatic transaction management to work correctly. When you're using manual transaction management,
    #  you're taking control of the transaction lifecycle, and on_commit() can't guarantee that the callback will be executed at the correct time.

    # due to manual transaction management the on_commit not worked and error will rise

    # to avoid this turn on the auto commit for this particular block then we can use the 'on_commit'

    transaction.set_autocommit(True)
    
    def send_email(args = None):
        print("---------send email called----------------",args)

    query1 = DBTransactions()
    query1.title = "trans 11"
    query1.description = "descript 11"
    query1.rating = 11
    query1.save()
    # transaction.commit()
    # transaction.on_commit(send_email)

    # Callbacks will not be passed any arguments, but you can bind them with functools.partial():

    from functools import partial
    
    transaction.on_commit(partial(send_email,args="working"))

    # 2------------f you call on_commit() while there isn’t an open transaction, the callback will be executed immediately.

    transaction.on_commit(partial(send_email,args="working"))

    # 3----------------------- robust=True

    # Passing robust=True can be useful in scenarios where you want to ensure that all callbacks are executed, 
    # even if one of them fails. This can help prevent cascading failures and ensure that your application remains in a consistent state.

    # If one on-commit function registered with robust=False within a given transaction raises an uncaught exception, no later registered functions in that same transaction will run

    def robust_test(args):
        raise ValidationError

    transaction.on_commit(partial(robust_test,args="robust working"),robust=True)

    transaction.on_commit(partial(send_email,args="robust working"),robust=True)

    return render(request,"learning_orm_queries/index.html",{"db_trans":result})


def learn_save_point(request):

    result = []

    #1---------outer transaction // inner transaction

    from django.db import transaction
    from functools import partial

    def call(c):
        print("----call----",c)

    # here the two on_commit events will be called

    with transaction.atomic(): #outer transaction #start a new transaction 
        transaction.on_commit(partial(call,c = "outer transaction"))
        with transaction.atomic(): #inner transaction #create a savepoint
            transaction.on_commit(partial(call,c = "inner transaction"))

    # here the no commit events will be called because the on_commit will be called after leaving the atomic block
    
    # but here even the outer atomic block has no error but inside atomic having error so the two callback functions will not be happen

    # with transaction.atomic(): #outer transaction #start a new transaction 
    #     transaction.on_commit(partial(call,c = "outer transaction"))
    #     with transaction.atomic(): #inner transaction #create a savepoint
    #         transaction.on_commit(partial(call,c = "inner transaction"))
    #         raise Exception("Exception rised")
        
    #if i handle the error the outer block event and inner block evnet also will be called

    # Your callbacks are executed after a successful commit, so a failure in a callback will not cause the transaction to roll back.

    with transaction.atomic(): #outer transaction #start a new transaction 
        transaction.on_commit(partial(call,c = "outer transaction"))
        with transaction.atomic(): #inner transaction #create a savepoint
            try:
                transaction.on_commit(partial(call,c = "inner transaction"))
                raise Exception("Exception rised")
            except Exception:
                pass
    # On-commit functions only work with autocommit mode and the atomic() (or ATOMIC_REQUESTS) transaction API. Calling on_commit() when autocommit is disabled and you are not within an atomic block will result in an error.


    ##-2--------------Order of execution¶
    # On-commit functions for a given transaction are executed in the order they were registered.

    #3----------------get auto commit enabled or not


    transaction_status = transaction.get_autocommit() #it will take using as args which is a db name , if not given default db will be taken

    print("----------trans status---",transaction_status)

    #4----------we can explicitly set auto commit fales or true using

    transaction.set_autocommit(False) #it will take using as args which is a db name , if not given default db will be taken

    # one auto commit turned of we can use func to commit or rollback

    transaction.commit()

    transaction.rollback()

    # we can manually create save points to rollback

    sid = transaction.savepoint() #it will return sid by using this we can rollback the transactions

    print("--------sid----------------",sid)

    transaction.rollback(sid)

    # we can also use commit

    transaction.commit(sid)

    # clear all the save points

    transaction.clean_savepoints()

    # Savepoints may be used to recover from a database error by performing a partial rollback. If you’re doing this inside an atomic() block, the entire block will still be rolled back, because it doesn’t know you’ve handled the situation at a lower level! 
    # To prevent this, you can control the rollback behavior with the following functions.

    transaction.get_rollback()


    # get_rollback(using=None)¶

    # set_rollback(rollback, using=None)¶

    # Setting the rollback flag to True forces a rollback when exiting the innermost atomic block. This may be useful to trigger a rollback without raising an exception.

    # Setting it to False prevents such a rollback. Before doing that, make sure you’ve rolled back the transaction to a known-good savepoint within the current atomic block! Otherwise you’re breaking atomicity and data corruption may occur.

    transaction.savepoint_commit(sid)

    transaction.savepoint_rollback(sid)
    
    return render(request,"learning_orm_queries/index.html",{"db_trans":result})

from customer.models import *

def learn_multi_databases(request):

    result = []

    # when there is no default databse is configured and even the databse_routers defined in settings , 
    # we can override it by usling 'using'  keywork like below 

    # result = Customer.objects.using("sql_lite_db").all()

    # result = Customer.objects.using("postgresql_db").all()


    # 2---------------we can use using in save method also
    # like save(using = "db name")

    # #--------------for delete we can use
    #result = Customer.objects.using("postgresql_db").get(pk=1)
    # result.delete() or result.delete(using="db name")

    # 3------------ when use custom manager we can't use like below

    # why we can't use 'using' in the custom manager with custom method means the 'after using the custom method is not available/accessable' 

    # result = Customer.custom_manager.using("sql_lite_db").all() #this is possible because of the 'all' is 'objects' inherited method.

    # result = Customer.custom_manager.using("sql_lite_db").get_all() #this is not possible error will rise

    # to overcome this we can use 'db_manager'

    # db_manager is used to select the database and hold all the custom manager methods

    result = Customer.custom_manager.db_manager("sql_lite_db").get_all()

    result = Customer.mg_q.db_manager("sql_lite_db").get_all_rec()

    print("-------result--manager---------",result)

    # --3 use multi database in cursor

    from django.db import connections

    with connections["postgresql_db"].cursor() as cursor:
        cursor.execute(" SELECT * FROM customer_customer")
        
        # when using dynamic params do not include '' quotes in query like '%s' use only %s
        
        # cursor.execute(" SELECT * FROM customer_customer where name=%s",['Gopi'])

        # row = cursor.fetchone()
        all_row = cursor.fetchall()
        # many_row = cursor.fetchmany()
        # print("---fetch one---",row)
        print("---fetch all--",all_row)
        # print("---fetch many_row--",many_row)

    # result = []

    return render(request,"learning_orm_queries/index.html",{"db_trans":result})


def from_youtube(request):
    pass
    # 1
    # cripsy_form
    # honeypot
    # default django login,register forms
    # 404page not found in set in settiings.py

    # 2
    # templates - include
    # namespace for routing use in python file
    # use form name and send input val in get method to get the val in route  method
    # back routing by using jinja result.meta.http.

    # 3 
    # login required decorator
    # UsercreationForm() django default forms

    #4
    # timesince pip use in inside the templating in html file like {{creation  | timesince}} it will give result like 3 min ago


from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.http import JsonResponse
from django.db.models import F,Q
from django.contrib.auth.forms import AuthenticationForm
from .forms import *

# Create your views here.

def get_corrected_words_list(word):
    from spellchecker import SpellChecker
    from textblob import TextBlob
    import re
    pattern = r'[^a-zA-Z0-9\s]'
    word = re.sub(pattern,'',word)
    spell_check = SpellChecker()
    words = []
    most_like = spell_check.correction(word)
    if most_like:
        words += list(most_like)
    possible_words = spell_check.candidates(word)
    if possible_words:
        words += list(possible_words)
    text_b = TextBlob(word)
    w = text_b.correct()
    if w:
        words.append(str(w))
    return words

def get_search_data(search_text):
    from whoosh.index import open_dir
    import os
    from django.conf import settings
    from whoosh.qparser import MultifieldParser
    whoosh_folder_name = "whoosh_search"
    path = os.path.join(settings.BASE_DIR,whoosh_folder_name)
    if os.path.exists(path):
        product_ids = []
        ix = open_dir(path)
        for tx in search_text:
            query = MultifieldParser(["product_name"],ix.schema).parse(tx)
            with ix.searcher() as search:
                result = search.search_page(query,pagenum=1)
                if result:
                    for r in result:
                        if r.get("name"):
                            product_ids.append(int(r.get("name")))
        return product_ids
    return None

def product_list(request):
    data = []
    search_txt = ''
    if request.method == "GET":
        search_txt = request.GET.get("search-txt")
    if search_txt:
        corrected_words_list = search_txt.split(" ")
        for tx in search_txt.split(" "):
            corrected_words_list += get_corrected_words_list(tx)
        corrected_words_list = list(set(corrected_words_list))

        print("-------corrected_words_list----------->",corrected_words_list)
        
        ids = get_search_data(corrected_words_list)

        print("-------ids------------------>",ids)

        if ids:
            data = Product.objects.filter(pk__in = ids)
    else:
        data = Product.objects.all()
    # print("-------request.user------------------>",request.user)

    if request.user:
        for d in data:
            cart = Cart.objects.filter(customer = request.user,product_id = d.id).values("qty","id")
            # print("-------cart------------------>",cart)
            if cart:
                d.cart_qty = cart[0].get("qty")
                d.cart_id = cart[0].get("id") 
    # print("-------search_txt----------->",search_txt.split("+"))
    return render(request,"ecommerce_app/pages/product-list.html",{"data":data,"auth":1 if request.user.is_authenticated else 0,"search_txt":search_txt})

def add_to_cart(request):
    try:
        if request.POST.get("cart_id") or Cart.objects.filter(customer = request.user):
            if request.POST.get("cart_id"):
                cart = Cart.objects.get(id = request.POST.get("cart_id"))
            else:
                cart = Cart.objects.get(customer = request.user)
            cart.qty += 1
            cart.save()
        else:
            cart = Cart()
            cart.customer = request.user
            cart.product_id = request.POST.get("product_id")
            cart.product_name = request.POST.get("product_name")
            cart.product_image = request.POST.get("url")
            cart.price = request.POST.get("price")
            cart.old_price = request.POST.get("old_price")
            cart.qty = 1
            cart.save()
            print("=--------------cart------------------>",cart.id)
        # return redirect("/ecommerce_app/product-list")
        return JsonResponse({"status":"success"}, status=200)
        # return JsonResponse({'message': 'Created'}, status=201)  # 201 Created
    except Exception as e:
        print("----------------e=------->",e)
        return JsonResponse({"status":"failed"}, status=500)
    

def delete_cart(request):
    try:
        if request.POST.get("cart_id"):
            cart = Cart.objects.get(id = request.POST.get("cart_id"))
            cart.qty -= 1
            cart.save()
        else:
            return JsonResponse({"status":"failed","message":"Cart id missing."})
        # return redirect("/ecommerce_app/product-list")
        return JsonResponse({"status":"success"}, status=200)
        # return JsonResponse({'message': 'Created'}, status=201)  # 201 Created
    except Exception as e:
        print("----------------e=------->",e)
        return JsonResponse({"status":"failed"}, status=500)

from django.contrib import messages
def sign_up(request):
    from django.contrib.auth.models import User
    form = None
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("-----------form--------------->",form)
            form.save()
            messages.success(request,"Signup successfully.")
            form = UserCreationForm()
        # else:
        #     print("-----------form.errors--------------->",form.errors)
        #     messages.error(request,form.errors)
    else:
        form = UserCreationForm()
    return render(request,"ecommerce_app/pages/signup.html",{"form":form})

def log_in(request):


    from django.db import connection

    with connection.cursor() as cursor:

        cursor.execute("""
                        SELECT * FROM ecommerce_app_product P INNER JOIN ecommerce_app_cart C ON C.product_id = P.id
                    """)

        rows = cursor.fetchall()

        fields = [col[0] for col in cursor.description]

        print("--------zip--->",dict(zip(fields,rows[0])))

        print("----------description----------->",cursor.description)

        print("----------res[]----------->",rows)


    from django.contrib.auth import authenticate,login
    if request.method == "POST":
        form = AuthenticationForm(request,data = request.POST)
        print("---------valid----------------------------->",form.is_valid())
        if form.is_valid():
            auth = authenticate(username = form.cleaned_data.get("username"),password=form.cleaned_data.get("password"))
            if auth:
                login(request,auth)
                messages.success(request,"Logged in success!")
                print("---------loggre\din----------------------------->")
        # else:
        #     print("---------errors----------------------------->",form.errors)
        #     form = AuthenticationForm()
            # messages.error(request,form.errors)
    else:
        form = AuthenticationForm()
    return render(request,"ecommerce_app/pages/login.html",{"form":form})

def add_cart_by_id(request,cart_id):
    print("-------cartid",cart_id)
    return render(request,"ecommerce_app/pages/product-list.html",{"data":[Cart.objects.get(pk=int(cart_id))],"auth":1 if request.user.is_authenticated else 0,"search_txt":"search_txt"})
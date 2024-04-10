from django.shortcuts import render,redirect,HttpResponse,get_object_or_404,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from product_management.models import Product,Article2,Book,Tag
from django.template import loader
from django.http import Http404,HttpResponse,HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import generic


class IndexView(generic.ListView):
    model = Tag
    template_name = "customer/list_view.html"
    context_object_name = "tag"
    paginate_by = 1


    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Tag.objects.order_by("id")[:5]

class DetailView(generic.DetailView):
    model = Tag
    template_name = "customer/detail_view.html"
    context_object_name = "tag"









cust_templates = "customer/templates"
cust_static = "customer/static"

# Create your views here.


def register(request):
    if request.method == "POST":
        messages.info(request,"working well")
        # return render(request, f"{cust_templates}/register.html",{"user":request.user})
        if request.POST["username"] and request.POST["password"]:
            username = request.POST["username"]
            password = request.POST["password"]
            # k = UserCreationForm(request.POST)
            # if k.is_valid():
            #     k.save()
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect("/customer/login")
        else:
            if not request.POST["username"]:
                return render(request, f"{cust_templates}/register.html",{"message":"Username is required"})
            if not request.POST["password"]:    
                return render(request, f"{cust_templates}/register.html",{"message":"Password is required"})
    else:
        return render(request, f"{cust_templates}/register.html")
    
def login(request):
    if request.method == "POST":
        info = request.POST
        if info.get('username') and info.get('password'):
            auth = authenticate(username = info.get('username'), password = info.get('password'))
            return redirect("/customer/register")
    return render(request, f"{cust_templates}/login.html")

def dynamic_url(request,id,iff):
    # raise Http404("page does not exist")
    obj = Tag.objects.all()
    # from customer.serializers import ProductModelSerializer
    # s_resp = ProductModelSerializer(obj,many = True)
    # print(s_resp.data)
    for ob in obj:
        ob = Tag.objects.get(id=ob.id)
        ob.all_books = ob.articles.all()
        print("0b--------------",ob)
        print("--------------onj",ob.articles.all())
    # print("---------obj",type(obj))
    # obj = get_object_or_404(Product,pk=id)
    # obj = Product.objects.get(id=id)
    # return render(request,f"customer/test.html",{'obj':obj})
    template = loader.get_template("customer/test.html")
    context = {"obj":obj[0] ,"l":"lititle"}
    return HttpResponse(template.render(context,request))



# ...
def vote(request, question_id):
    question = get_object_or_404(Product, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "customer/test.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
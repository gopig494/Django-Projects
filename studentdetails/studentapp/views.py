from django.shortcuts import render
from studentapp.models import studentdetails
from studentapp.form import fdetails
from django.shortcuts import redirect
# Create your views here.

def check(request):
	details=studentdetails.objects.all()
	dir={"data":details}
	return render (request,'studentapp/index.html',context=dir)


def sfor(request):
	store=fdetails()
	dier={'forms':store}
	if request.method =='POST':
		form=fdetails(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/studentapp/check')
	return render(request,'studentapp/forms.html',context=dier)

def delete(request,id):
	details=studentdetails.objects.get(id=id)
	details.delete()
	return redirect('/studentapp/check')
	
	
def update(request,id):
	details=studentdetails.objects.get(id=id)
	dic={"update":details}
	if request.method =='POST':
		form=fdetails(request.POST,instance=details)
		if form.is_valid():
			form.save()
			return redirect('/studentapp/check')
	return render (request ,'studentapp/update.html',context=dic)
	
	
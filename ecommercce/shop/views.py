from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from shop.models import Category
class Categories(View):
    def get(self, request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request, 'categories.html',context)

class Products(View):
    def get(self, request,i):
        c=Category.objects.get(id=i)
        context={'category':c}

        return render(request,'products.html',context)
from shop.forms import SignUpForm,LoginForm
class Register(View):

    def post(self,request):


        form_instance = SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()

            return redirect('shop:categories')

    def get(self,request):
        form_instance=SignUpForm()
        context={'form':form_instance}
        return render(request,'register.html',context)

from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
class Login(View):
    def post(self,request):
        form_instance=LoginForm(request.POST)
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            print(data)
            u=data['username']
            p=data['password']
            #authenticate()
            user=authenticate(username=u,password=p)
            if user:
                login(request,user)  #adds user to session


                return redirect('shop:categories')
            else:
                messages.error(request,'invalid user credentials')
                return redirect('shop:login')

    def get(self,request):
        form_instance = LoginForm()
        context={'form':form_instance}
        return render(request,'login.html',context)


class Logout(View):
    def get(self,request):
        logout(request) #removes user from the session
        return redirect('shop:login')

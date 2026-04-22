from django.shortcuts import render,redirect
from django.views import View
# Create your views here.
from shop.models import Category

class Categories(View):
    def get(self, request):
        c=Category.objects.all()
        context={'categories':c}
        return render(request, 'categories.html',context)

class Productslist(View):
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
        context={'form':form_instance}
        return render(request, 'register.html', context )

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




from shop.models import Products
from shop.forms import CategoryForm, ProductForm, StockForm

# Add Category
class AddCategory(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = CategoryForm()
            return render(request, 'add_category.html', {'form': form})
        messages.error(request, "You are not authorized to access this page.")
        return redirect('shop:categories')

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Category added successfully!")
                return redirect('shop:categories')
            return render(request, 'add_category.html', {'form': form})



# Add Product
class AddProduct(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = ProductForm()
            return render(request, 'add_product.html', {'form': form})


    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Product added successfully!")
                return redirect('shop:categories')
            return render(request, 'add_product.html', {'form': form})



class ProductDetail(View):
    def get(self,request,i):
        p=Products.objects.get(id=i)
        context = {'product': p}
        return render(request, 'product_detail.html',context)


class AddStock(View):
    def get(self, request, i):
        if request.user.is_authenticated and request.user.is_superuser:
            p = Products.objects.get(id=i)
            form = StockForm(instance=p)  # Load current stock
            return render(request, 'addstock.html', {'form': form, 'product': p})


    def post(self, request, i):
        if request.user.is_authenticated and request.user.is_superuser:
            p = Products.objects.get(id=i)
            form = StockForm(request.POST, instance=p)  # Update stock
            if form.is_valid():
                form.save()
                return redirect('shop:productdetails', i=i)
            return render(request, 'addstock.html', {'form': form, 'product': p})

from django.shortcuts import render,redirect
from django.views import View
from shop.models import Products
from django.db.models import Q

class Search(View):
    def get(self,request):
        query=request.GET.get('q')
        print(query)                       #keyword to search


        p=Products.objects.filter(Q(name__icontains=query) |
                              Q(description__icontains=query) |
                              Q(price__icontains=query))
        context={'products':p}

        #filter query
        #Model lookups
        # __contains
        #QObject




        return render(request, 'search.html',context)














































# from django.shortcuts import render
# from django.views import View
# from shop.models import Products
# from .forms import SearchForm
#
# class SearchView(View):
#     def get(self, request):
#         form = SearchForm()
#         context = {'form': form}
#         return render(request, 'search.html', context)
#
#     def post(self, request):
#         form = SearchForm(request.POST)
#         if form.is_valid():
#             q = form.cleaned_data['query']
#             results = Products.objects.filter(name__icontains=q)
#             context = {'form': form, 'results': results, 'query': q}
#             return render(request, 'search.html', context)
#         context = {'form': form}
#         return render(request, 'search.html', context)


# from django.urls import path
# from . import views
#
# app_name = "search"
#
# urlpatterns = [
#     path('', views.SearchView.as_view(), name='search'),
# ]
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





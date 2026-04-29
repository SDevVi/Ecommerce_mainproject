from django.shortcuts import render, redirect
from django.views import View
from .forms import OrderForm
from .models import Cart
from shop.models import Products
import razorpay
import uuid
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class AddToCart(View):
    def get(self, request, i):

        u=request.user #logged in user
        p=Products.objects.get(id=i)  #product selected by user

        try:
            c=Cart.objects.get(user=u,product=p)  #checks whether the specified product
                                                  #already added by user

            c.quantity+=1    #if yes, increments its quantity by 1
            c.save()

        except:     #else creates a new cart record with quantity 1
            c=Cart.objects.create(user=u,product=p,quantity=1)
            c.save()

        return redirect('cart:cartview')

class CartView(View):
    def get(self, request):
        u=request.user
        c=Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total = total+(i.product.price * i.quantity)


        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

class CartDecrement(View):
    def get(self, request,i):
        try:
            c=Cart.objects.get(id=i)
            if c.quantity>1:
               c.quantity-=1
               c.save()

            else:
                c.delete()
        except:
            pass
        return redirect('cart:cartview')

class CartRemove(View):
    def get(self, request,i):
        try:
            print(i)
            c = Cart.objects.get(id=i)
            print(c)
            c.delete()
        except:
            pass

        return redirect('cart:cartview')

class Checkout(View):
    def get(self, request):
        form_instance=OrderForm()
        context={'form':form_instance}
        return render(request,'checkout.html',context)


    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)

            user=request.user
            u.user= user


            c=Cart.objects.filter(user=user)
            total=0
            for i in c:
               total= total+(i.product.price * i.quantity)

            u.amount= float(total)
            u.save()
            if(u.payment_method == "Online"):
                #creates a razorpay client connection using keys
                 client=razorpay.Client(auth=("rzp_test_SeUpldVV1gbP9W","omuXXA6Hb7ktzeAr0Y4HdThF"))

                #creates a new order in razorpay
                 response_payment=client.order.create({'amount':int(u.amount*100),'currency':'INR'})


                 print(response_payment)
                 #Retrieve the order id from response payment
                 id= response_payment['id']

                # adds to the order record stored in our db table
                 u.order_id=id
                 u.save()
                 context={'payment':response_payment}
                 return render(request, 'payment.html', context)


            else:#COD
                 id = uuid.uuid4().hex[:14]
                 i = 'order_COD'+id
                 u.order_id=i
                 u.is_ordered = True
                 u.save()

                 c = Cart.objects.filter(user=u.user)
                 for i in c:
                     item = OrderItems.objects.create(order=u,product=i.product,quantity=i.quantity,price=i.product.price)
                     item.save()


                 c.delete()
                 return render(request,'payment.html')



from .models import Order, OrderItems

@method_decorator(csrf_exempt,name='dispatch')
class PaymentSuccess(View):
    def post(self, request):
        response=request.POST
        print(response)

        # after successful payment mark order as True


        id = response['razorpay_order_id']
        o = Order.objects.get(order_id=id)   #fetches the corresponding order from the database using the order ID
        o.is_ordered = True       #(Order completed like marking)
        o.save()

         #(User cart items all taken)
        c=Cart.objects.filter(user=o.user)

        #This loops through each item in the cart.
        for i in c:
            #(Cart → OrderItems  converting)
            items=OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity,price=i.product.price)
            items.save()



        #deletes the cart
        c.delete()

        return render(request, 'payment_success.html')


class OrderSummary(View):
    def get(self, request):
        u=request.user
        o = Order.objects.filter(user=u, is_ordered=True)
        context={'orders':o}
        return render(request, 'order_summary.html',context)






















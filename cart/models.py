from django.db import models
from django.contrib.auth.models import User
from shop.models import Products
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return  self.quantity * self.product.price

    def __str__(self):
        return self.user.username



class Order(models.Model):


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(null=True,max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100, unique=True, editable=False, default=uuid.uuid4)
    ordered_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=15)

    is_ordered = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, null=True)
    delivery_status = models.CharField(max_length=20,default='pending',null=True)





    def __str__(self):
        return self.order_id


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.order_id


from django.db import models

class Category(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='categories')


    def __str__(self):
        return self.name

class Products(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    image=models.ImageField(upload_to='products')
    stock=models.IntegerField()
    price=models.IntegerField()
    available = models.IntegerField(default=True)

    category = models.ForeignKey(Category,on_delete=models.CASCADE, related_name='category')

    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

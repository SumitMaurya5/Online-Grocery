from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Registeration(models.Model):
    Firstname =models.CharField(max_length=200)
    Lastname =models.CharField(max_length=200)
    Email=models.EmailField()
    Mobile=models.PositiveIntegerField()
    Address=models.TextField()
    Pincode=models.IntegerField()
    City=models.CharField(max_length=20)
    State=models.CharField(max_length=20)
    Country=models.CharField(max_length=20)
    Password=models.CharField(max_length=200)

    def _str_(self):
        return self.Firstname


class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    ful_name=models.CharField(max_length=50)

    def __str__(self):
        return self.ful_name


class Category(models.Model):
    title=models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Products(models.Model):
    title=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="products")
    marked_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    description=models.TextField()
    available = models.BooleanField(default=True)

class Coupan(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_form = models.DateTimeField()
    Valid_to = models.DateTimeField()
    Discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    active = models.BooleanField()

    def __str__(self):
        return self.code


class Cart(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total=models.PositiveIntegerField(default=0)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart:" + str(self.id)


class CartProduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal= models.PositiveIntegerField()

    def __str__(self):
        return "Cart:" + str(self.cart.id) + "CartProduct:" + str(self.id)


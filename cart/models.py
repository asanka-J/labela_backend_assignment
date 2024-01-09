from django.db import models
from django.contrib.auth.models import User
from product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=50, unique=True, blank=True, null=True)
    
    def __str__(self):
        return f"{self.cart_id}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    class Meta: #ensure that a product can only be added once
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.id}"


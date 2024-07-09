from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False)
    image = models.ImageField(upload_to='product_images/')
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)

    def get_total(self):
        total = sum(item.get_total() for item in self.items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)

    def get_total(self):
        return self.price * self.quantity

    def get_total(self):
        return self.price * self.quantity

from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = (
    ("store_owner", "Store Owner"),
    ("staff", "Staff"),
    ("customer", "Customer"),
)

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=100, blank=True)
    domain = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    vendor = models.ForeignKey(Vendor, null=True, blank=True, on_delete=models.CASCADE, related_name='users')

    def is_store_owner(self):
        return self.role == 'store_owner'

    def is_staff_role(self):
        return self.role == 'staff'

    def is_customer_role(self):
        return self.role == 'customer'

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    assigned_to = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_products')

    def __str__(self):
        return f"{self.name} ({self.vendor})"

class Order(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='assigned_orders')
    status = models.CharField(max_length=20, default='pending')

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity
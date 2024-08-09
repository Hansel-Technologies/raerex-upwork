from django.db import models
from django.conf import settings
from shop.models import Product

class EquipmentCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ServiceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(default='example@example.com')    
    phone = models.CharField(max_length=20, default='+254-000-0000')   
    equipment = models.ManyToManyField('Equipment')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    description = models.TextField()
    equipment_photo = models.ImageField(upload_to='service_requests/', blank=True, null=True)
    preferred_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Service Request #{self.id} by {self.name}"
    
class Quote(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote for Service Request {self.service_request.id}"
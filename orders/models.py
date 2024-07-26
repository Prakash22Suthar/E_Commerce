from django.db import models

from base.models import BaseModel
from users.models import User
from products.models import Product
# Create your models here.

# class OrderUpdates(models.Model):
#     update_status = models.DateTimeField(null=True, blank=True)

class Orders(BaseModel):

    """
    This model is used to track status of an order with order details : unique_id, order_by, items, status

    """

    PENDING = "pending"
    PROCESSING = "processing"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"
    DELIVERED = "delivered"

    order_status = (
        (PENDING,"Pending"),
        (CONFIRMED,"Confirmed"),
        (DELIVERED,"Delivered"),
        (CANCELED, "Canceled"),
    )

    order_id = models.CharField(max_length=255, unique=True)
    order_created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=50, choices=order_status,default=PENDING)
    delevery_address = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.order_id

class Orderitem(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_item")
    items = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="order_item")
    quantity = models.PositiveIntegerField(default=0)
    amount = models.FloatField(null=True, blank=True)
    
    

from django.contrib import admin

from .models import Orders
# Register your models here.


@admin.register(Orders)
class Orders(admin.ModelAdmin):
    list_display = ["id", "order_number", "created_by","status"]
    list_display_links = ["order_number"]
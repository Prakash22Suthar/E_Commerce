from django.contrib import admin

from .models import User
# Register your models here.

 
@admin.register(User)
class Users(admin.ModelAdmin):
    list_display = ["id","username","mobile_no", "email"]
    list_display_links = ["username"]
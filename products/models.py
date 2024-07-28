from django.db import models

from base.models import BaseModel

# Create your models here.

class Category(models.Model):
    """
    This model will save category name and its description
    """
    name = models.CharField(max_length=255, unique= True)
    description = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class Subcategory(models.Model):
    """
    This model will save Subcategory of category with subcategory info : name and its description
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_category")

    def __str__(self) -> str:
        return self.name


class Product(BaseModel):
    """
    This model holds information about every product : name, description, unique_code, image, 
    category, subcategory
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    product_code = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="products/images/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(null=True, blank=True, default=0)
    weight = models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self) -> str:
        return self.name
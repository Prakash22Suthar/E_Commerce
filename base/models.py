from django.db import models

# Create your models here.

class BaseModel(models.Model):

    """
    This base model for the other table to track when the entity are created.
    Also When they are modified
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
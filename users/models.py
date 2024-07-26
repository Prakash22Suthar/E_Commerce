from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from base.models import BaseModel
# Create your models here.

# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None):
#         """
#         Creates and saves a User with the given email and password.
#         """
#         if not email:
#             raise ValueError("Users must have an email address")

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_staffuser(self, email, password):
#         """
#         Creates and saves a staff user with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#         )
#         user.staff = True
#         user.admin = True
#         user.save(using=self._db)
#         return user


class User(AbstractUser, BaseModel):
    """
    This is a custom user model where extra field added to AbstactUser Model added fieds are:
    mobile_no, dob, gender, address, profile_pic
    """

    MALE = "m"
    FEMALE = "f"
    OTHER = "o"
    G_Choices = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )
    email = models.EmailField(max_length=150, unique=True)
    mobile_no = models.IntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=G_Choices, blank=True, null=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="users/profile_pic/", null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default it need to be write because we change username field .
    # objects = UserManager()

    def __str__(self) -> str:
        return self.get_full_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
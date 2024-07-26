from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, exceptions

from django.contrib.auth import authenticate, get_user_model

from .models import User

class UsersSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name","last_name","username","email","password","mobile_no","gender","address","dob","profile_pic"]
        extra_kwargs = {"password":{"write_only":True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        attrs["email"] = attrs.get("email","").lower()
        self._authenticate(attrs.get("email"), attrs.get("password"))

        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["id"] = self.user.id
        data["full_name"] = self.user.get_full_name
        data["email"] = self.user.email
        
        return data

    
    def _authenticate(self, email, password):
        user = User.objects.filter(email=email).last()

        if not user:
            raise exceptions.AuthenticationFailed({"email_error":"Please enter your registered email"})
        
        if not authenticate(**{get_user_model().USERNAME_FIELD: email, "password":password}):
            raise exceptions.AuthenticationFailed({"password_error":"Password is incorrect, please try again"})
        
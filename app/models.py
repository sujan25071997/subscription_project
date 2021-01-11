from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class UserProfileManager(BaseUserManager):

    def create_user(self,email,name,password=None):
        '''create a new user profile'''
        if not email:
            raise ValueError('User must have a email address')

        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name,password):
        '''create a new superuser profile'''
        user = self.create_user(email,name,password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database models for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    """Email will be uses as Username"""
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        '''Retrieve full name of user'''
        return self.name

    def get_short_name(self):
        '''Retrieve shot name of user'''
        return self.name

    def __str__(self):
        return self.email


class StripeSubscription(models.Model):
    start_date = models.DateTimeField(help_text="The start date of the subscription.")
    status = models.CharField(max_length=20, help_text="The status of this subscription.")
    # other data we need about the Subscription from Stripe goes here


class MyStripeModel(models.Model):
    name = models.CharField(max_length=100)
    stripe_subscription = models.ForeignKey(StripeSubscription, on_delete=models.CASCADE)

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone



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
    stripe_subscription = models.ForeignKey(StripeSubscription, on_delete=models.DO_NOTHING,)

class CurrentSubscription(models.Model):
    customer = models.OneToOneField(
        UserProfile,
        related_name="current_subscription",
        null=True, on_delete=models.DO_NOTHING,
    )
    plan = models.CharField(max_length=100)
    quantity = models.IntegerField()
    start = models.DateTimeField()
    # trialing, active, past_due, canceled, or unpaid
    status = models.CharField(max_length=25)
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(blank=True, null=True)
    current_period_end = models.DateTimeField(blank=True, null=True)
    current_period_start = models.DateTimeField(blank=True, null=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    trial_end = models.DateTimeField(blank=True, null=True)
    trial_start = models.DateTimeField(blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=10, default="usd")
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def total_amount(self):
        return self.amount * self.quantity

    def plan_display(self):
        return PAYMENTS_PLANS[self.plan]["name"]

    def status_display(self):
        return self.status.replace("_", " ").title()

    def is_period_current(self):
        return self.current_period_end > timezone.now()

    def is_status_current(self):
        return self.status in ["trialing", "active"]

    def is_valid(self):
        if not self.is_status_current():
            return False

        if self.cancel_at_period_end and not self.is_period_current():
            return False

        return True

    def delete(self, using=None):  # pylint: disable=E1002
        """
        Set values to None while deleting the object so that any lingering
        references will not show previous values (such as when an Event
        signal is triggered after a subscription has been deleted)
        """
        super(CurrentSubscription, self).delete(using=using)
        self.plan = None
        self.status = None
        self.quantity = 0
        self.amount = 0

from django.contrib import admin
from .models import UserProfile,StripeSubscription,MyStripeModel

admin.site.register(UserProfile)
admin.site.register(StripeSubscription)
admin.site.register(MyStripeModel)

from django.contrib import admin
from .models import UserProfile,StripeSubscription,MyStripeModel,CurrentSubscription

admin.site.register(UserProfile)
admin.site.register(StripeSubscription)
admin.site.register(MyStripeModel)
admin.site.register(CurrentSubscription)

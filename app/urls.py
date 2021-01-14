from django.urls import path, include
from app import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user/', views.UserProfileViewSet, basename='user')
router.register('sub/', views.SubscriptionView, basename='sub')



urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.SignOut.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('thanks/', views.thanks, name='thanks'),
    path('checkout/', views.checkout, name='checkout'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('pricing_page/', views.pricing_page, name='pricing_page'),
    path('api/', include(router.urls)),
]

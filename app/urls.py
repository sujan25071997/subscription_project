from django.urls import path
from app import views

urlpatterns = [
    path('', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('', views.SignOut.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('thanks/', views.thanks, name='thanks'),
    path('checkout/', views.checkout, name='checkout'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('pricing_page/', views.pricing_page, name='pricing_page'),
]

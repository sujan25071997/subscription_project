from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib.auth import login
from .form import UserProfileForm
from django.views.generic.edit import CreateView
from .form import UserRegisterForm
from django.contrib.messages.views import SuccessMessageMixin

from django.views.generic.base import RedirectView
from django.contrib.auth import logout
#from django.core.urlresolvers import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist

from app import models
from app import serializers
from app import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserProfileSerializer, SubscriptionSerializer, MyStripeSerializer,
                            CurrentSubscriptionSerializer)


class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'registration\signup.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


class Login(LoginView):
    authentication_form = UserProfileForm
    form_class = UserProfileForm
    template_name = 'app/login.html'
    def form_valid(self, form):

        if self.request.user.is_authenticated():
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None and user.is_active:
                login(self.request, user)
                return super(LoginView, self).form_valid(form)
            else:
                return self.form_invalid(form)


class SignOut(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self):
        logout(self.request)
        return reverse('signup')

def pricing_page(request):
    return render(request, 'pricing_page.html', {
        'products': Product.objects.all()
    })

stripe.api_key = settings.STRIPE_PRIVATE_KEY

def index(request):
    return render(request, 'app/index.html')

def thanks(request):
    return render(request, 'app/thanks.html')

@csrf_exempt
def checkout(request):
    # Create Strip Checkout
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1I71XkBYUZLKpHL5NSgszcTD',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('index')),
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })


@csrf_exempt
def checkoutm(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1I7kePBYUZLKpHL5imY347PS',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('thanks')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('index')),
    )

    return JsonResponse({
        'session_id' : session.id,
        'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
    })


@csrf_exempt
def stripe_webhook(request):

    print('WEBHOOK!')
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = 'whsec_Xj8wBk2qiUcjDEmYu5kfKkOrJCJ5UUjW'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items)

    return HttpResponse(status=200)




##################################################################
#Django Restframework

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name','email',)


class StripeView(APIView):
    """ Generic API StripeView """
    permission_classes = (IsAuthenticated, )

    def get_current_subscription(self):
        try:
            return self.request.user.customer.current_subscription
        except CurrentSubscription.DoesNotExist:
            return None

    def get_customer(self):
        try:
            return self.request.user.customer
        except ObjectDoesNotExist:
            return Customer.create(self.request.user)


class SubscriptionView(StripeView):
    """ See, change/set the current customer/user subscription plan """
    serializer_class = SubscriptionSerializer

    def get(self, request, *args, **kwargs):
        current_subscription = self.get_current_subscription()
        serializer = CurrentSubscriptionSerializer(current_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                stripe_plan = validated_data.get('stripe_plan', None)
                customer = self.get_customer()
                subscription = customer.subscribe(stripe_plan)

                return Response(subscription, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except stripe.StripeError as e:
            from django.utils.encoding import smart_str

            error_data = {u'error': smart_str(e) or u'Unknown error'}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

    '''Adding a dummy get_extra_actions classmethod'''
    @classmethod
    def get_extra_actions(cls):
        return []

from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('payment/<str:amount>/', views.billing, name='payment'),
    path('complete_payment', views.complete_payment, name='complete_payment'),
    path('payment_success', views.payment_success, name='payment_success')
]

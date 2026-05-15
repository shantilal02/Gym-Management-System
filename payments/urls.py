from django.urls import path
from . import views

urlpatterns = [
    path('', views.payments_list, name='payments_list'),
    path('record/', views.payment_record, name='payment_record'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.summary_view, name='summary_view'),
    path('export/', views.export_txt, name='export_txt'),
]

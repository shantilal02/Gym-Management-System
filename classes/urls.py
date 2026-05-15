from django.urls import path
from . import views

urlpatterns = [
    path('', views.classes_list, name='classes_list'),
    path('create/', views.class_create, name='class_create'),
    path('<int:cid>/enroll/', views.class_enroll, name='class_enroll'),
    path('<int:cid>/delete/', views.class_delete, name='class_delete'),
]

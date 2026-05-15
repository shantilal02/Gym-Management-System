from django.urls import path
from . import views

urlpatterns = [
    path('', views.members_list, name='members_list'),
    path('create/', views.member_create, name='member_create'),
    path('<int:mid>/edit/', views.member_edit, name='member_edit'),
    path('<int:mid>/delete/', views.member_delete, name='member_delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipment_list, name='equipment_list'),
    path('add/', views.equipment_add, name='equipment_add'),
    path('<int:eid>/delete/', views.equipment_delete, name='equipment_delete'),
]

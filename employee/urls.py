from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_view, name='create_view'),
    path('create_emp/', views.create_emp, name='create_emp'),
    path('update/<int:id>/', views.update_view, name='update_view'),
    path('update/update_emp/<int:id>/', views.update_emp, name='update_emp'),
    path('delete_emp/<int:id>/', views.delete_emp, name='delete_emp'),
]
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import EmployeeListAPI

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_view, name='create_view'),
    path('create_emp/', views.create_emp, name='create_emp'),
    path('update/<int:id>/', views.update_view, name='update_view'),
    path('update/update_emp/<int:id>/', views.update_emp, name='update_emp'),
    path('delete_emp/<int:id>/', views.delete_emp, name='delete_emp'),

    path('trash/', views.trash_view, name='trash_view'),
    path('restore/<int:id>/', views.restore_emp, name='restore_emp'),
    path('permanent_delete/<int:id>/', views.permanent_delete_emp, name='permanent_delete'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),

    path('api/employees/', EmployeeListAPI.as_view(), name='employee_api'),
    path('api/employees/<int:pk>/', views.EmployeeDetailAPI.as_view(), name='employee_detail_api'),
]
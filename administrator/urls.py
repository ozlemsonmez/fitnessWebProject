from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("administrator", views.administrator, name="administrator"),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('delete-user/', views.delete_user, name='delete_user'),
    path('register/', views.register, name='register'),
]

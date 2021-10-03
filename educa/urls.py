from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView, name='login'),
    path('accounts/logout', auth_views.LogoutView, name='logout'),
    path('admin/', admin.site.urls),
]

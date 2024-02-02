"""
URL configuration for YankinPedOPDMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from common.views import base_view
from UserAuthentication.views import login_view, logout_view, doctor_view, unauthorized_view, admin_view, nurse_view, pharmacist_view, receptionist_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', base_view, name='base'),
    path('login/', login_view, name='login'),
    path('dashboard/', base_view, name = 'dashboard'),
    path('logout/', logout_view, name='logout'),
    path('doctor/', doctor_view, name = 'doctor_dashboard'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
    path('admin_dash/', admin_view, name = 'admin_dashboard'),
    path('nurse/', nurse_view, name = 'nurse_dashboard'),
    path('pharmacist/', pharmacist_view, name = 'pharmacist_dashboard'),
    path('receptionist/', receptionist_view, name = 'receptionist_dashboard'),
]

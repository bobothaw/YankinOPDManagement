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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from common.views import base_view
from UserAuthentication.views import login_view, logout_view, doctor_view, unauthorized_view, admin_view, nurse_view, pharmacist_view, receptionist_view
from NurseApp.views import waitingList_view
from DoctorApp.views import docPatQueueView
from PharmacistApp.views import medicine_insert
from ReceptionApp.views import patient_insert_view
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('doctor/', docPatQueueView, name = 'doctor_dashboard'),
    path('unauthorized/', unauthorized_view, name='unauthorized'),
    path('admin_dash/', admin_view, name = 'admin_dashboard'),
    path('nurse/', waitingList_view, name = 'nurse_dashboard'),
    path('pharmacist/', medicine_insert, name = 'pharmacist_dashboard'),
    path('receptionist/', patient_insert_view, name = 'receptionist_dashboard'),
    path('ReceptionApp/', include('ReceptionApp.urls')),
    path('NurseApp/', include('NurseApp.urls')),
    path('PharmacistApp/', include('PharmacistApp.urls')),
    path('DoctorApp/', include('DoctorApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

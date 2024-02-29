from django.urls import path
from .views import docPatQueueView

urlpatterns = [
    path('docPatQueue/', docPatQueueView, name='docPatQueue')
]

from django.urls import path
from .views import docPatQueueView, diagnosisView

urlpatterns = [
    path('docPatQueue/', docPatQueueView, name='docPatQueue'),
    path('diagnosis/<int:waitingID>', diagnosisView, name='diagnose'),
]

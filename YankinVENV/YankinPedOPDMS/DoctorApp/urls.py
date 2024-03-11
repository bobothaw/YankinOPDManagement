from django.urls import path
from .views import docPatQueueView, diagnosisView, diagnosisRecord

urlpatterns = [
    path('docPatQueue/', docPatQueueView, name='docPatQueue'),
    path('diagnosis/<int:waitingID>', diagnosisView, name='diagnose'),
    path('diagnosisRecord/<int:waitingID>', diagnosisRecord, name='diagnoserecord'),
]

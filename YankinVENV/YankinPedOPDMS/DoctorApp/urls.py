from django.urls import path
from .views import docPatQueueView, diagnosisView, diagnosisRecord, diagnosisEdit, diagnosisHistoryView

urlpatterns = [
    path('docPatQueue/', docPatQueueView, name='docPatQueue'),
    path('diagnosis/<int:waitingID>', diagnosisView, name='diagnose'),
    path('diagnosisRecord/<int:waitingID>', diagnosisRecord, name='diagnoserecord'),
    path('diagnosisEdit/<int:diagnosisID>', diagnosisEdit, name='diagnosisedit'), 
    path('diagnosisHistory/', diagnosisHistoryView, name='diagHistory'),
]

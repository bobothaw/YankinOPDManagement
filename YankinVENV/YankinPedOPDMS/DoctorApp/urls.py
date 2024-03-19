from django.urls import path
from .views import docPatQueueView, diagnosisView, diagnosisRecord, diagnosisEdit, diagnosisHistoryView, diagnosisUpdate,admissionView, admissionDelete

urlpatterns = [
    path('docPatQueue/', docPatQueueView, name='docPatQueue'),
    path('diagnosis/<int:waitingID>', diagnosisView, name='diagnose'),
    path('diagnosisRecord/<int:waitingID>', diagnosisRecord, name='diagnoserecord'),
    path('diagnosisEdit/<int:diagnosisID>', diagnosisEdit, name='diagnosisedit'), 
    path('diagnosisHistory/', diagnosisHistoryView, name='diagHistory'),
    path('diagnosisUpdate/<int:diagnosisID>', diagnosisUpdate, name='diagUpdate'),
    path('admissions/', admissionView, name='admitView'),
    path('admissionDelete/<int:admissionID>', admissionDelete, name='admitDelete'),
]

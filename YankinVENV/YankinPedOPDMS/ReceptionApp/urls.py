from django.urls import path
from .views import patient_insert_view, patient_list_view, edit_patient_view, patientEdit, patient_search, queue_view,today_queue_view, all_queue_view, delete_queue_view


urlpatterns = [
    path('patientinsert/', patient_insert_view, name = 'patientInsert'),
    path('patientlist/', patient_list_view, name='patientList'),
    path('patientedit/<int:patient_id>/', edit_patient_view, name='edit_view'),
    path('patientrealedit/<int:patient_id>/', patientEdit, name='patientEdit'),
    path('patientsearch/', patient_search, name="patientSearch"),
    path('patientqueue/<int:patient_id>/', queue_view, name='patientQueue'),
    path('todayqueue/', today_queue_view, name='todayqueue'),
    path('allqueue/', all_queue_view, name="allqueue"),
    path('deletequeue/<int:waitinglist_id>', delete_queue_view, name="deletequeue"),
]

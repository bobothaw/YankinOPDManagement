from django.urls import path
from .views import waitingList_view, record_view, edit_view, ready_list


urlpatterns = [
    path('nurseQueue/', waitingList_view, name='nurseQueue'),
    path('nurseRecord/<int:waitingID>/', record_view, name='nurseRecord'),
    path('nurseReadyList/', ready_list, name="readyList"),
    path('nurseEdit/<int:waitingID>/', edit_view, name="nurseEdit"),
]


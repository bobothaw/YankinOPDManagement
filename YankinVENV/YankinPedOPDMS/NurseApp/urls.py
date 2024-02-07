from django.urls import path
from .views import waitingList_view


urlpatterns = [
    path('nurseQueue/', waitingList_view, name='nurseQueue'),
]


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ReceptionApp.models import WaitingList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from datetime import date
from .models import Diagnosis, Ward


# Create your views here.
@login_required
def docPatQueueView(request):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    context = {
        'waitingLists': waitingLists,
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'DoctorApp/doctor-patient-queue.html', context)


@login_required
def diagnosisView(request, waitingID):
    user = request.user
    waitingPatient = get_object_or_404(WaitingList, pk=waitingID)
    diaglist = Diagnosis.objects.all()
    wards = Ward.objects.all()
    context = {
        'waitingPatient': waitingPatient,
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
        'diaglist': diaglist,
        'wards': wards,
    }
    return render(request, 'DoctorApp/diagnosispage.html', context)



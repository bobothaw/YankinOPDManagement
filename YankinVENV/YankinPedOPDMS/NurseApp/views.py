from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ReceptionApp.models import WaitingList
from datetime import date
from django.conf import settings


# Create your views here.
@login_required
def waitingList_view(request):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = False).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'NurseApp/nurse-dashboard.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def record_view(request, waitingID):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = False).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    waitingList = get_object_or_404(WaitingList, pk=waitingID)
    if request.method == 'POST':
        try:
            waitingList.temperature = request.POST.get('temp')
            waitingList.weight = request.POST.get('weight')
            waitingList.systole = request.POST.get('systole')
            waitingList.diastole = request.POST.get('diastole')
            waitingList.isReady = True
            waitingList.last_edit_by = user
            waitingList.save()
            return render(request, 'NurseApp/nurse-dashboard.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL, 'success_message': "The patient's vital sign is recorded successfully."})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'NurseApp/nurse-dashboard.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL, 'error_message': error_message})
    else:
        return render(request, 'NurseApp/nurse-record.html', {'waitingItem': waitingList, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

def ready_list(request):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'NurseApp/nurse-ready-list.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def edit_view(request, waitingID):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    waitingList = get_object_or_404(WaitingList, pk=waitingID)
    if request.method == 'POST':
        try:
            waitingList.temperature = request.POST.get('temp')
            waitingList.weight = request.POST.get('weight')
            waitingList.systole = request.POST.get('systole')
            waitingList.diastole = request.POST.get('diastole')
            waitingList.isReady = True
            waitingList.last_edit_by = user
            waitingList.save()
            return render(request, 'NurseApp/nurse-ready-list.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL, 'success_message': "The patient's vital sign is updated successfully."})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'NurseApp/nurse-ready-list.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL, 'error_message': error_message})
    else:
        return render(request, 'NurseApp/nurse-edit.html', {'waitingItem': waitingList, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})
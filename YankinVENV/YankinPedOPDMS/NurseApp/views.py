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
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today()).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'NurseApp/nurse-dashboard.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def record_view(request, waitingID):
    user = request.user
    waitingList = get_object_or_404(WaitingList, pk=waitingID)
    if request.method == 'POST':
        waitingList.temperature = request.POST.get('')


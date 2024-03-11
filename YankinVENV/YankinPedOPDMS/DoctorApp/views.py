from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ReceptionApp.models import WaitingList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from datetime import date
from .models import Diagnosis, Ward, PrescribedMedicine, DiagnosisDetails
from PharmacistApp.models import Medicine


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
    medicines = Medicine.objects.all()

    context = {
        'waitingPatient': waitingPatient,
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
        'diaglist': diaglist,
        'wards': wards,
        'medicines':medicines,
    }
    return render(request, 'DoctorApp/diagnosispage.html', context)

@login_required
def diagnosisRecord(request, waitingID):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    try:
        if request.method == 'POST':
            chief_conplaint = request.POST.get('cheifCon')
            secondary_conplaint = request.POST.get('secCon')
            physical_findings = request.POST.get('phyFind')
            test_results = request.POST.get('testResult')
            primary_diagnosis = get_object_or_404(Diagnosis, pk=request.POST.get('primaryDiag'))
            secondary_diagnosis = get_object_or_404(Diagnosis, pk=request.POST.get('secondaryDiag'))
            waitingList = get_object_or_404(WaitingList, pk=waitingID)
            diagnosedBy = user
            newDiagDetail = DiagnosisDetails(
                chief_conplaint=chief_conplaint, 
                secondary_conplaint=secondary_conplaint, 
                physical_findings=physical_findings,
                test_results=test_results, 
                primary_diagnosis=primary_diagnosis, 
                secondary_diagnosis=secondary_diagnosis, 
                waitingList=waitingList, 
                diagnosedBy=diagnosedBy)
            newDiagDetail.save()
            medicines = request.POST.getlist('prescription[]')
            quantities = request.POST.getlist('quantity[]')
            instructions = request.POST.getlist('instruction[]')
            
            for medicine, quantity, instruction in zip(medicines, quantities, instructions):
                newPrescribedMedicine = PrescribedMedicine(
                    relatedDiagDetail=get_object_or_404(DiagnosisDetails, pk=newDiagDetail.id),
                    medicine=get_object_or_404(Medicine, pk=medicine),
                    quantity=quantity,
                    instruction=instruction
                )
                newPrescribedMedicine.save()
            context = {
                'waitingLists': waitingLists,
                'user':user,
                'MEDIA_URL': settings.MEDIA_URL,
                'success_message':'The patient is diagnosed successfully'
            }
            return render(request, 'DoctorApp/doctor-patient-queue.html', context)
    except Exception as e:
        error_message = f"Error: {e}"
        context = {
            'waitingLists': waitingLists,
            'user':user,
            'MEDIA_URL': settings.MEDIA_URL,
            'error_message':error_message
        }
        return render(request, 'DoctorApp/doctor-patient-queue.html', context)



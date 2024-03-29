from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from ReceptionApp.models import WaitingList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from datetime import date
from .models import Diagnosis, Ward, PrescribedMedicine, DiagnosisDetails, Admission
from PharmacistApp.models import Medicine


# Create your views here.
@login_required
def docPatQueueView(request):
    user = request.user
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True, isDiagnosed = False).order_by('queue_date_time')
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
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today(), isReady = True, isDiagnosed = False).order_by('queue_date_time')
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

            if request.POST.get('admitCheck') == 'True':
                newAdmission = Admission(
                    admission_reason=request.POST.get('admit-reason'),
                    admitted_ward = get_object_or_404(Ward, pk=request.POST.get('ward')),
                    related_diag_detail=newDiagDetail
                    )
                newAdmission.save()
            waitingList.isDiagnosed = True
            waitingList.save()
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

@login_required 
def diagnosisEdit(request, diagnosisID):
    user = request.user
    wards = Ward.objects.all()
    medicines = Medicine.objects.all()
    diagnosis = get_object_or_404(DiagnosisDetails, pk=diagnosisID)
    waitingID = diagnosis.waitingList.id
    waitingPatient = get_object_or_404(WaitingList, pk=waitingID)
    prescribedmedicines = PrescribedMedicine.objects.filter(relatedDiagDetail_id=diagnosisID)
    admissionsQuery = Admission.objects.filter(related_diag_detail_id=diagnosisID)
    admission = admissionsQuery.first()
    diaglist = Diagnosis.objects.all()
    context = {
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
        'wards':wards,
        'medicines':medicines,
        'prescribedmedicines':prescribedmedicines,
        'admission':admission,
        'diagnosis':diagnosis,
        'diaglist': diaglist,
        'waitingPatient': waitingPatient,
    }
    return render(request, 'DoctorApp/diagnosisedit.html', context)

@login_required
def diagnosisHistoryView (request):
    user = request.user
    diagnosisQuery = DiagnosisDetails.objects.filter(
        waitingList__consult_date = date.today(),
        waitingList__isDiagnosed = True,
    ).order_by('diagnosed_datetime')
    paginator = Paginator(diagnosisQuery, 10)
    diagnosisLists = paginator.get_page(request.GET.get('page', 1))
    context = {
        'diagnosisLists':diagnosisLists,
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'DoctorApp/diagnosed-queue.html', context)

@login_required
def diagnosisUpdate(request, diagnosisID):
    user = request.user
    diagnosisQuery = DiagnosisDetails.objects.filter(
        waitingList__consult_date = date.today(),
        waitingList__isDiagnosed = True,
    ).order_by('diagnosed_datetime')
    paginator = Paginator(diagnosisQuery, 10)
    diagnosisLists = paginator.get_page(request.GET.get('page', 1))
    context = {
        'diagnosisLists':diagnosisLists,
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    try:
        
        diagnosisObject = get_object_or_404(DiagnosisDetails, pk=diagnosisID)
        if request.method == 'POST':
            diagnosisObject.chief_conplaint = request.POST.get('cheifCon')
            diagnosisObject.secondary_conplaint = request.POST.get('secCon')
            diagnosisObject.physical_findings = request.POST.get('phyFind')
            diagnosisObject.test_results = request.POST.get('testResult')
            diagnosisObject.primary_diagnosis = get_object_or_404(Diagnosis, pk=request.POST.get('primaryDiag'))
            diagnosisObject.secondary_diagnosis = get_object_or_404(Diagnosis, pk=request.POST.get('secondaryDiag'))
            
            diagnosisObject.save()
            medicines = request.POST.getlist('prescription[]')
            quantities = request.POST.getlist('quantity[]')
            instructions = request.POST.getlist('instruction[]')
            
            existing_prescriptions = PrescribedMedicine.objects.filter(relatedDiagDetail=diagnosisObject)
            existing_prescriptions.delete()
            
            for medicine, quantity, instruction in zip(medicines, quantities, instructions):
                newPrescribedMedicine = PrescribedMedicine(
                    relatedDiagDetail=get_object_or_404(DiagnosisDetails, pk=diagnosisObject.id),
                    medicine=get_object_or_404(Medicine, pk=medicine),
                    quantity=quantity,
                    instruction=instruction
                )
                newPrescribedMedicine.save()

            if request.POST.get('admitCheck') == 'True':
                admissionQuery = Admission.objects.filter(
                    related_diag_detail_id = diagnosisObject.id
                )
                admissionObject = admissionQuery.first()
                admissionObject.admission_reason = request.POST.get('admit-reason')
                admissionObject.admitted_ward = get_object_or_404(Ward, pk=request.POST.get('ward'))
                admissionObject.save()
            context['success_message'] = "The diagnosis is updated successfully"
        return render(request, 'DoctorApp/diagnosed-queue.html', context)
    except Exception as e:
        error_message = f"Error: {e}"
        context['error_message'] = error_message
        return render(request, 'DoctorApp/diagnosed-queue.html', context)
    

@login_required
def admissionView(request):
    user = request.user
    admissionsQuery = Admission.objects.filter(is_discharged = False)
    paginator = Paginator(admissionsQuery, 10)
    admissions = paginator.get_page(request.GET.get('page', 1))
    context = {
        'user': user,
        'admissions': admissions,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render(request, 'DoctorApp/admission-view.html', context)

@login_required
def admissionDelete(request, admissionID):
    user = request.user
    admissionsQuery = Admission.objects.filter(is_discharged = False)
    paginator = Paginator(admissionsQuery, 10)
    admissions = paginator.get_page(request.GET.get('page', 1))
    context = {
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
        'admissions':admissions,
    }
    try:
        admissionObejct = get_object_or_404(Admission, pk=admissionID)
        admissionObejct.delete()
        context['success_message']="The admission of the patient has been successfully deleted."
        return render(request, 'DoctorApp/admission-view.html', context)
    except Exception as e:
        error_message = f"Error: {e}"
        context['eror_message'] = error_message
        return render(request, 'DoctorApp/admission-view.html', context)
        

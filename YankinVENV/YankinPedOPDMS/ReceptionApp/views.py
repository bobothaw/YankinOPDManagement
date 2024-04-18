from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Patient, WaitingList
from django.db.models import Q
from datetime import date, datetime
from django.conf import settings
# Create your views here.

today_date = date.today().strftime('%Y-%m-%d')

@login_required
def patient_insert_view(request):
    user = request.user
    if request.method == 'POST':
        patient_name = request.POST.get('FullName')
        date_of_birth = request.POST.get('DOB')
        gender = request.POST.get('GenderRadio')
        if request.POST.get('NRC')=='':
            NRCnum = None
        else:
            NRCnum = request.POST.get('NRC')
        father_name = request.POST.get('FatherName')
        mother_name = request.POST.get('MotherName')
        guardian_name = request.POST.get('GuardianName')
        relationship = request.POST.get('Relationship')
        address = request.POST.get('Address')
        insert_by = user
        last_edit_by = user

        try:
            newPatient = Patient(patient_name = patient_name, date_of_birth=date_of_birth, gender=gender, 
            NRCnum=NRCnum, father_name=father_name, mother_name=mother_name, guardian_name=guardian_name, 
            relationship=relationship, address=address, insert_by=insert_by, last_edit_by=last_edit_by)
            
            newPatient.save()
            if request.POST.get('QueueCheck') == 'True':
                Patient.objects.first()
                newqueue = WaitingList(patient=newPatient, insert_by=insert_by, last_edit_by=last_edit_by)
                newqueue.save()
            
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'success_message':'The patient data is inserted successfully.', 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL})
            
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'error_message':error_message, 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL})
 
@login_required
def patient_list_view(request):
    user = request.user
    original_patients = Patient.objects.all()

    # Get the search query from the GET parameters
    query = request.GET.get('patientSearch', '')

    if query:
        # If there's a search query, filter the patients
        search_results = original_patients.filter(
            Q(patient_name__icontains=query) |
            Q(NRCnum__icontains=query) |
            Q(date_of_birth__icontains=query)
        )
        paginator = Paginator(search_results, 10)
        try:
            patients = paginator.page(request.GET.get('page', 1))
        except PageNotAnInteger:
            patients = paginator.page(1)
        except EmptyPage:
            patients = paginator.page(paginator.num_pages)
    else:
        # If no search query, use the original patient list for pagination
        paginator = Paginator(original_patients, 10)
        try:
            patients = paginator.page(request.GET.get('page', 1))
        except PageNotAnInteger:
            patients = paginator.page(1)
        except EmptyPage:
            patients = paginator.page(paginator.num_pages)

    return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user': user, 'query': query, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def patient_search(request):
    user = request.user
    query = request.POST.get('patientSearch', '')
    patients_query_set = Patient.objects.filter(
        Q(patient_name__icontains=query) |
        Q(NRCnum__icontains=query) |
        Q(date_of_birth__icontains=query)
    )
    paginator = Paginator(patients_query_set, 10)
    patients = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def edit_patient_view(request, patient_id):
    user = request.user
    patient = get_object_or_404(Patient, pk=patient_id)
    # You can add the logic for updating patient data here
    return render(request, 'ReceptionApp/reception-edit.html', {'patient': patient, 'today_date': today_date, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def patientEdit (request, patient_id):
    user = request.user
    patient = get_object_or_404(Patient, pk=patient_id)
    if request.method =='POST':
        patient.patient_name = request.POST.get('FullName')
        patient.date_of_birth = request.POST.get('DOB')
        patient.gender = request.POST.get('GenderRadio')
        patient.NRCnum = request.POST.get('NRC')
        patient.father_name = request.POST.get('FatherName')
        patient.mother_name = request.POST.get('MotherName')
        patient.guardian_name = request.POST.get('GuardianName')
        patient.relationship = request.POST.get('Relationship')
        patient.address = request.POST.get('Address')
        patient.last_edit_by = user
        patients = Patient.objects.all()
        try:
            patient.save()
            return render(request, 'ReceptionApp/reception-edit.html', {'user': user, 'success_message':'The patient data is edited successfully. Check ID: '+ str(patient.id) , 'patients': patients, 'MEDIA_URL': settings.MEDIA_URL})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user': user, 'error_message': error_message, 'MEDIA_URL': settings.MEDIA_URL})

@login_required      
def queue_view(request, patient_id):
    user = request.user
    patient = get_object_or_404(Patient, pk=patient_id)
    patientsall = Patient.objects.all()
    paginator = Paginator(patientsall, 10)
    patients = paginator.get_page(request.GET.get('page', 1))
    try:
        newqueue = WaitingList(patient=patient, insert_by=user, last_edit_by=user)
        newqueue.save() 
        return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user': user, 'success_message': "The patient is queued in today's list successfully.", 'MEDIA_URL': settings.MEDIA_URL})
    except Exception as e:
        error_message = f"Error: {e}"
        return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user': user, 'error_message': error_message, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def today_queue_view (request):
    user = request.user
    
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today()).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))        
    return render(request, 'ReceptionApp/reception-queue.html', {'waitingLists': waitingLists, 'user':user, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def delete_queue_view(request, waitinglist_id):
    user = request.user
    queue_patient = get_object_or_404(WaitingList, pk=waitinglist_id)
    waitingListQuery = WaitingList.objects.filter(consult_date = date.today()).order_by('queue_date_time')
    paginator = Paginator(waitingListQuery, 10)
    waitingLists = paginator.get_page(request.GET.get('page', 1))
    try:
        queue_patient.delete()
        return render(request, 'ReceptionApp/reception-queue.html', {'waitingLists': waitingLists, 'user': user, 'success_message': 'Patient removed from waiting list successfully!', 'MEDIA_URL': settings.MEDIA_URL})
    except Exception as e:
        error_message = f"Error: {e}"
        return render(request, 'ReceptionApp/reception-queue.html', {'waitingLists': waitingLists, 'user': user, 'error_message': error_message, 'MEDIA_URL': settings.MEDIA_URL})

@login_required
def all_queue_view (request):
    user = request.user
    allwaitingList = WaitingList.objects.all()
    
    query = request.GET.get('queueSearch', '')

    if query:
        try:
            search_date = datetime.strptime(query, '%Y-%m-%d').date()
            # Filter the WaitingList queryset
            waitingListQuery = WaitingList.objects.filter(consult_date=search_date)
        except ValueError:
        # Handle if the query is not a valid date
        # For example, you can ignore the date search and only search for the patient name
            waitingListQuery = WaitingList.objects.filter(
                patient__patient_name__icontains=query
            )
        paginator = Paginator(waitingListQuery, 10)
        waitingLists = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'ReceptionApp/reception-queue.html', {'waitingLists': waitingLists, 'today_date': today_date, 'user':user, 'query': query, 'request': request, 'MEDIA_URL': settings.MEDIA_URL})
    else:
        paginator = Paginator(allwaitingList, 10)
        waitingLists = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'ReceptionApp/reception-queue.html', {'waitingLists': waitingLists, 'today_date': today_date, 'user':user, 'request': request, 'MEDIA_URL': settings.MEDIA_URL})
    


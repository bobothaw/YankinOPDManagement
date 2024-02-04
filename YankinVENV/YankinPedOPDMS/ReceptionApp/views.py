from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Patient, WaitingList
from datetime import date
# Create your views here.

today_date = date.today().strftime('%Y-%m-%d')

@login_required
def patient_insert_view(request):
    user = request.user
    if request.method == 'POST':
        patient_name = request.POST.get('FullName')
        date_of_birth = request.POST.get('DOB')
        gender = request.POST.get('GenderRadio')
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
            
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'success_message':'The patient data is inserted successfully.', 'today_date': today_date})
            
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'error_message':error_message, 'today_date': today_date})
    else:
        return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'today_date': today_date})
 
def patient_list_view(request):
    user = request.user

    patients = Patient.objects.all()

    paginator = Paginator(patients, 10)

    page = request.GET.get('page', 1)
    try:
        patients = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        patients = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, show the last page
        patients = paginator.page(paginator.num_pages)

    return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user':user})

def edit_patient_view(request, patient_id):
    user = request.user
    patient = get_object_or_404(Patient, pk=patient_id)
    # You can add the logic for updating patient data here
    return render(request, 'ReceptionApp/reception-edit.html', {'patient': patient, 'today_date': today_date, 'user':user})

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
            return render(request, 'ReceptionApp/reception-edit.html', {'user': user, 'success_message':'The patient data is edited successfully. Check ID: '+ str(patient.id) , 'patients': patients})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': today_date, 'user': user, 'error_message': error_message})
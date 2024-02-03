from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, WaitingList
from datetime import date
# Create your views here.

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
                Patient.objects.first();
                newqueue = WaitingList(patient=newPatient, insert_by=insert_by, last_edit_by=last_edit_by)
                newqueue.save()
            
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'success_message':'The patient data is inserted successfully.', 'today_date': date.today})
            
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'error_message':error_message, 'today_date': date.today})
    else:
        return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'today_date': date.today})
 
def patient_list_view(request):
    user = request.user
    patients = Patient.objects.all()
    return render(request, 'ReceptionApp/reception-edit.html', {'patients': patients, 'today_date': date.today, 'user':user})

def edit_patient(request, patient_id):
    user = request.user
    patient = get_object_or_404(Patient, pk=patient_id)
    # You can add the logic for updating patient data here
    return render(request, 'ReceptionApp/reception-edit.html', {'patient': patient, 'today_date': date.today, 'user':user})


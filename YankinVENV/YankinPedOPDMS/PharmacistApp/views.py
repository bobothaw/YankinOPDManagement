from django.shortcuts import render, get_object_or_404
from .models import Medicine, MedicineType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from datetime import date
from django.db.models import Q
from DoctorApp.models import DiagnosisDetails, PrescribedMedicine

today_date = date.today().strftime('%Y-%m-%d')
# Create your views here.
def medicine_insert(request):
    medTypes = MedicineType.objects.all()
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('medName')
        typeid = request.POST.get('medType')
        type = get_object_or_404(MedicineType, pk=typeid)
        dosage = request.POST.get('dosage')
        unit = request.POST.get('unit')
        stock = request.POST.get('stock')
        expiry_date = request.POST.get('expd')
        manufacturer = request.POST.get('manufacturer')
        price_per_unit = request.POST.get('price_per_unit')
        try:
            newMedicine = Medicine(name=name, type=type, dosage=dosage, unit=unit, stock=stock, 
                                   expiry_date=expiry_date, manufacturer=manufacturer, 
                                   price_per_unit=price_per_unit, added_by=user, updated_by=user)
            newMedicine.save()
            return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'success_message':'The medicine data is recorded successfully.', 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes, 'user':user})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'error_message':error_message, 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes, 'user':user})
    else:
        return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes, 'user':user})

def medicine_list(request):
    user = request.user
    medcines_list = Medicine.objects.all()
    paginator = Paginator(medcines_list, 10)
    medicines = paginator.get_page(request.GET.get('page', 1))
    query = request.GET.get('medicineSearch', '')

    if query:
        medicines_query_set = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(type__name__icontains=query) |
            Q(manufacturer__icontains=query)
        )
        paginator = Paginator(medicines_query_set, 10)
        medicines = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'PharmacistApp/pharmacy-medlist.html',{'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user, 'query':query})

    return render(request, 'PharmacistApp/pharmacy-medlist.html', {'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user})


def medicine_edit(request, medicineID):
    user = request.user
    medcines_list = Medicine.objects.all()
    paginator = Paginator(medcines_list, 10)
    medicines = paginator.get_page(request.GET.get('page', 1))
    medicine = get_object_or_404(Medicine, pk=medicineID)
    medTypes = MedicineType.objects.all()
    if request.method == 'POST':
        try:
            medicine.name = request.POST.get('medName')
            medicine.typeid = request.POST.get('medType')
            medicine.type = get_object_or_404(MedicineType, pk=medicine.typeid)
            medicine.dosage = request.POST.get('dosage')
            medicine.unit = request.POST.get('unit')
            medicine.stock = request.POST.get('stock')
            medicine.expiry_date = request.POST.get('expd')
            medicine.manufacturer = request.POST.get('manufacturer')
            medicine.price_per_unit = request.POST.get('price_per_unit')
            medicine.updated_by = user
            medicine.save()
            return render (request, 'PharmacistApp/pharmacy-medlist.html', {'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user, 'success_message': "The medicine information is updated successfully!"})
        except Exception as e:
            error_message = f"Error: {e}"
            return render (request, 'PharmacistApp/pharmacy-medlist.html', {'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user, 'error_message': error_message})

    return render (request, 'PharmacistApp/pharmacy-edit.html', {'MEDIA_URL': settings.MEDIA_URL, 'medicine':medicine, 'user':user, 'medTypes':medTypes})

def prescribedList(request):
    user = request.user
    diagnosisQuery = DiagnosisDetails.objects.filter(is_prescription_denied=None).order_by('diagnosed_datetime')
    paginator = Paginator(diagnosisQuery, 10)
    diagLists =  paginator.get_page(request.GET.get('page', 1))
    context = {
        'diagLists': diagLists,
        'user': user,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    return render (request, 'PharmacistApp/prescribed-list.html', context)

def presVerify(request, diagID):
    user = request.user
    diagnosis = get_object_or_404(DiagnosisDetails, pk=diagID)
    diagnosisQuery = DiagnosisDetails.objects.filter(Q(is_prescription_denied=None) | Q(is_prescription_denied=True)).order_by('diagnosed_datetime')
    paginator = Paginator(diagnosisQuery, 10)
    diagLists =  paginator.get_page(request.GET.get('page', 1))
    context = {
        'user':user,
        'MEDIA_URL': settings.MEDIA_URL,
    }
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'confirm':
            diagnosis.is_prescription_denied = False
            diagnosis.save()
        elif action == 'deny':
            diagnosis.is_prescription_denied = True
            diagnosis.save()
        context['diagLists'] = diagLists
        return render (request, 'PharmacistApp/prescribed-list.html', context)
    else:
        prescriptions = PrescribedMedicine.objects.filter(relatedDiagDetail = get_object_or_404(DiagnosisDetails, pk=diagID))
        context['prescriptions']=prescriptions
        context['diagnosis']= diagnosis
        return render(request, 'PharmacistApp/prescription-verify.html', context)

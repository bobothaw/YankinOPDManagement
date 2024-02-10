from django.shortcuts import render, get_object_or_404
from .models import Medicine, MedicineType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from datetime import date
from django.db.models import Q

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
        medicines_query_set = Medicine.object.filter(
            Q(name__icontains=query) |
            Q(MedicineType__name__icontains=query) |
            Q(manufacturer__icontains=query)
        )
        paginator = Paginator(medicines_query_set, 10)
        medicines = paginator.get_page(request.GET.get('page', 1))
        return render(request, 'PharmacistApp/pharmacy-medlist.html',{'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user})

    return render(request, 'PharmacistApp/pharmacy-medlist.html', {'MEDIA_URL': settings.MEDIA_URL, 'medicines':medicines, 'user':user})


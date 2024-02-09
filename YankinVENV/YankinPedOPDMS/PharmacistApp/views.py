from django.shortcuts import render, get_object_or_404
from .models import Medicine, MedicineType
from django.conf import settings
from datetime import date

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
            return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'success_message':'The medicine data is recorded successfully.', 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes})
        except Exception as e:
            error_message = f"Error: {e}"
            return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'error_message':error_message, 'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes})
    else:
        return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'today_date': today_date, 'MEDIA_URL': settings.MEDIA_URL, 'medTypes':medTypes})

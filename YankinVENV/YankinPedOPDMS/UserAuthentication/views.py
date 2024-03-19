from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from PharmacistApp.models import MedicineType

today_date = date.today().strftime('%Y-%m-%d')
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name='Admins').exists():
                return redirect('admin_dashboard')
                
            elif user.groups.filter(name='Doctors').exists():
                return redirect('doctor_dashboard')
            
            elif user.groups.filter(name='NurseAids').exists():
                return redirect('nurse_dashboard')
            
            elif user.groups.filter(name='Pharmacists').exists():
                return redirect('pharmacist_dashboard')
            
            elif user.groups.filter(name='Receptionists').exists():
                return redirect('receptionist_dashboard')
            
            else:
                return render(request, 'UserAuthentication/login.html', {'error_message': 'Invalid username or password'})
        else:
            return render(request, 'UserAuthentication/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'UserAuthentication/login.html')

#logout function
def logout_view(request):
    logout(request)
    return redirect('login')

def unauthorized_view(request):
    logout(request)
    return render(request, 'UserAuthentication/unauthorized.html')

def is_admin(user):
    return user.groups.filter(name='Admins').exists()

def is_doctor(user):
    return user.groups.filter(name='Doctors').exists()

def is_nurse(user):
    return user.groups.filter(name='NurseAids').exists()

def is_pharmacist(user):
    return user.groups.filter(name='Pharmacists').exists()

def is_receptionist(user):
    return user.groups.filter(name='Receptionists').exists()

@login_required
@user_passes_test(is_doctor, login_url='unauthorized')
def doctor_view(request):
    user = request.user
    return render(request, 'DoctorApp/doctor-patient-queue.html', {'user': user})

@login_required
@user_passes_test(is_admin, login_url='unauthorized')
def admin_view(request):
    user = request.user
    return render(request, 'AdminApp/admin-dashboard.html', {'user': user})

@login_required
@user_passes_test(is_nurse, login_url='unauthorized')
def nurse_view(request):
    user = request.user
    return render(request, 'NurseApp/nurse-dashboard.html', {'user': user})

@login_required
@user_passes_test(is_pharmacist, login_url='unauthorized')
def pharmacist_view(request):
    user = request.user
    medTypes = MedicineType.objects.all()
    return render(request, 'PharmacistApp/pharmacy-dashboard.html', {'user': user, "medTypes": medTypes, "today_date":today_date})

@login_required
@user_passes_test(is_receptionist, login_url='unauthorized')
def receptionist_view(request):
    today_date = date.today().strftime('%Y-%m-%d')
    user = request.user
    return render(request, 'ReceptionApp/reception-dashboard.html', {'user': user, 'today_date': today_date})





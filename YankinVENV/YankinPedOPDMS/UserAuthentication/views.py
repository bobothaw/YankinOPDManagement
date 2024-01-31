from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is valid, log them in
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other page
        else:
            # Invalid login credentials
            return render(request, 'UserAuthentication/login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'UserAuthentication/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    # The @login_required decorator ensures that only authenticated users can access this view.
    
    user = request.user  # You can directly access the authenticated user via request.user

    return render(request, 'dashboard.html', {'user': user})

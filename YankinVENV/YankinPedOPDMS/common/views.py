from django.shortcuts import render, redirect




# Create your views here.
def base_view(request):
    return render(request, 'common/base.html')



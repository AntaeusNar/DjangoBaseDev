from django.shortcuts import render

# Create your views here.


def dashboard(request):
    return render(request, 'service/dashboard.html')


def registration(request):
    return render(request, 'registration/register.html')

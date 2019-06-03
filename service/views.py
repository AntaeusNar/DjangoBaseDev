from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from service.forms import UserCreationForm
from service.models import Event

# Create your views here.


def dashboard(request):
    events = Event.objects.all
    context = {'events': events}
    return render(request, 'service/dashboard.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def create_event(request):
    return render(request, 'service/create_event.html')

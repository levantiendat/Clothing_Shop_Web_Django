from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Account

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            phone_number = form.cleaned_data.get('phone_number')
            role = 0
            account = Account.objects.create(user = user, name = name, phone_number = phone_number, role = role)
            account.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password = password)
            if user is not None:
                login(request, user)
                return redirect('signup')
            else:
                return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



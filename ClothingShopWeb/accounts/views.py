from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import Account
from django.contrib import messages

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

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            username = Account.objects.get(user=user).user.username
            request.session['user'] = username  # Lưu quyền của người dùng vào session
            return redirect('category_list')  # Chuyển hướng đến trang shop
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')



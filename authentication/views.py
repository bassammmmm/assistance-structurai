from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
import re
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
                return redirect('login')
        else:
            messages.error(request, 'Please fill all information.')
            return redirect('login')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        context = {
            'username' : username,
            'email' : email
        }
        if not username:
            messages.error(request, 'Username is required.')
            return render(request, 'register.html', context)
        if not email:
            messages.error(request, 'Email address is required.')
            return render(request, 'register.html', context)
        if not bool(re.match(email_regex, email)):
            messages.error(request, 'Please write a valid email address.')
            return render(request, 'register.html', context)
        if not password1:
            messages.error(request, 'Password is required.')
            return render(request, 'register.html', context)
        if not password2:
            messages.error(request, 'Password is required.')
            return render(request, 'register.html', context)
        if not password1 == password2:
            messages.error(request, 'Please make sure passwords match.')
            return render(request, 'register.html', context)

        if username:
            if User.objects.filter(username=username):
                messages.error(request, 'An account with this username already exists. Please try another username.')
                return render(request, 'register.html', context)
            elif (len(password1) < 6):
                messages.error(request, 'Password is too short.')
                return render(request, 'register.html', context)
            else:
                user = User.objects.create(username=username, email=email)
                user.set_password(password1)
                user.save()
                user = authenticate(username=username, password=password1)
                if user:
                    login(request, user)
                    return redirect('home')
    return render(request, 'register.html')
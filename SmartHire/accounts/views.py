from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from django.contrib.auth.models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not username or not not password:
            messages.error(request, 'All fields are required')
            return render(request, 'accounts/register.html')
        
        
        if not password or not not confirm_password:
            messages.error(request, 'Password do not match')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
                return render(request, 'accounts/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'email is already registered.')
            return render(request, 'accounts/register.html')
        
        # Create user and hash password automatically
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('job_list')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('job_list')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'accounts/login.html')

    return render(request, 'accounts/login.html')
        
        
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out')
    return redirect('job_list')
        
        
        
        
        


        

        
        
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from account_app.models import User
from django.contrib import messages


# Create your views here.
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(user.get_user_type())
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return redirect(request.path)
    if request.method == 'GET':
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user_type = request.POST.get('user_type')
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username not available')
            return redirect('register')
        if user_type == 'job_seeker':
            User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                     password=password, is_job_seeker=True)
        elif user_type == 'recruiter':
            User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                     password=password, is_job_seeker=True)
        return render(request, 'register.html')
    if request.method == 'GET':
        return render(request, 'register.html')


def resume(request):
    return render(request, 'resume.html')


def user_logout(request):
    logout(request)
    return redirect('sign_in')

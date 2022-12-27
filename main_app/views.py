from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from account_app.models import User
from django.contrib import messages
from .forms import ResumeForm
from datetime import date


# Create your views here.
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_job_seeker:
                login(request, user)
                return redirect('resume')
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
        messages.add_message(request, messages.SUCCESS, 'Account Created Successfully')
        return render(request, 'register.html')
    if request.method == 'GET':
        return render(request, 'register.html')


def resume(request):
    context = {}
    if request.method == "POST":
        form = ResumeForm(request.POST)
        if form.is_valid():
            temp = form.save()
            date_of_birth = temp.date_of_birth
            today = date.today()
            age = today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            print(age)
            return redirect('resume')
        else:
            context['form'] = form
            return render(request, 'resume.html', context)
    form = ResumeForm()
    context['form'] = form
    return render(request, 'resume.html', context)


def user_logout(request):
    logout(request)
    return redirect('sign_in')


def job_seeker_dashboard(request):
    # only display this page if user is job seeker and logged in
    if request.user.is_job_seeker and request.user.is_authenticated:
        return render(request, 'job_seeker_dashboard.html')


def recruiter_dashboard(request):
    # only display this page if user is recruiter and logged in
    if request.user.is_recruiter and request.user.is_authenticated:
        return render(request, 'recruiter_dashboard.html')

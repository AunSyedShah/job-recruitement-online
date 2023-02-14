from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from account_app.models import User
from django.contrib import messages
from .forms import ResumeForm, JobPostedForm, SearchCandidateForm
from datetime import date
from .models import Resume, JobPosted
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_job_seeker:
                # if resume already exists, redirect to job seeker dashboard
                if Resume.objects.filter(user=user).exists():
                    return redirect('job_seeker_dashboard')
                return redirect('resume')
            elif user.is_recruiter:
                return redirect('recruiter_dashboard')
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
        if user_type == 'recruiter':
            User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                     password=password, is_recruiter=True)
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
            temp.user = request.user
            today = date.today()
            age = today.year - date_of_birth.year - (
                    (today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            form.save()
            # store age in session
            request.session['age'] = age
            return redirect('job_seeker_dashboard')
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


def post_job(request):
    if request.user.is_recruiter and request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            form = JobPostedForm(request.POST)
            if form.is_valid():
                temp = form.save()
                temp.job_posted_by = request.user
                form.save()
                return redirect('recruiter_dashboard')
            else:
                context['form'] = form
                return render(request, 'post_job.html', context)
        if request.method == "GET":
            context['form'] = JobPostedForm()
            return render(request, 'post_job.html', context)
        return render(request, 'post_job.html')


def jobs_posted(request):
    if request.user.is_recruiter and request.user.is_authenticated:
        posted_jobs = JobPosted.objects.filter(job_posted_by=request.user)
        context = {'jobs_posted': posted_jobs}
        return render(request, 'jobs_posted.html', context)
    return redirect('sign_in')


def search_candidates(request):
    if request.user.is_recruiter and request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            if 'job_sector' in request.POST:
                print(request.POST)
                form = SearchCandidateForm(request.POST)
                if form.is_valid():
                    job_sector = form.cleaned_data['job_sector']
                    candidates = Resume.objects.filter(job_sector=job_sector)
                    context['candidates'] = candidates
                    context['form'] = SearchCandidateForm()
                    return render(request, 'search_candidates.html', context)
                else:
                    context['form'] = form
                    return render(request, 'search_candidates.html', context)
            if 'select_btn' in request.POST:
                print(request.POST)
                candidate_id = request.POST.get('candidate_id')
                candidate = Resume.objects.get(id=candidate_id)
                candidate.is_selected = True
                candidate.selected_by = request.user
                candidate.save()
                messages.add_message(request, messages.SUCCESS, 'Candidate Selected')
                return redirect('search_candidates')
        if request.method == "GET":
            context['form'] = SearchCandidateForm()
            return render(request, 'search_candidates.html', context)
        return render(request, 'search_candidates.html')


def view_candidate(request, profile_id):
    if request.user.is_recruiter and request.user.is_authenticated:
        candidate = Resume.objects.get(id=profile_id)
        context = {'candidate': candidate}
        return render(request, 'view_candidate_profile.html', context)
    return redirect('sign_in')


# mark candidate as selected, API request
@csrf_exempt
def select_candidate(request):
    # request body to json
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    profile_id = body['candidate_id']
    candidate = Resume.objects.get(id=profile_id)
    candidate.is_selected = True
    candidate.save()
    return JsonResponse({'success': True})

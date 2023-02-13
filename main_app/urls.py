from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('resume/', views.resume, name='resume'),
    path('logout/', views.user_logout, name='logout'),
    path('job_seeker_dashboard/', views.job_seeker_dashboard, name='job_seeker_dashboard'),
    path('recruiter_dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('post_job/', views.post_job, name='post_job'),
    path('jobs_posted/', views.jobs_posted, name='jobs_posted'),
    path('search_candidates/', views.search_candidates, name='search_candidates'),
    path('view_candidate/<int:profile_id>', views.view_candidate, name='view_candidate'),
    path('select_candidate/', views.select_candidate, name='select_candidate'),
]

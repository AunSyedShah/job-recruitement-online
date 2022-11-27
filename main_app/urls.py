from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('register/', views.register, name='register'),
    path('resume/', views.resume, name='resume'),
    path('logout/', views.user_logout, name='logout'),
]

from django.db import models
from account_app.models import User


class JobPosted(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_sector_choices = (
        (1, 'Accountancy, Banking and Finance'),
        (2, 'Engineering and Manufacturing'),
        (3, 'Agriculture'),
        (4, 'Health'),
        (5, 'Property and Construction'),
        (6, 'Education'),
    )
    job_sector = models.IntegerField(choices=job_sector_choices, default=1)
    job_type_choices = (
        (1, 'Full Time'),
        (2, 'Part Time'),
        (3, 'Contract'),
        (4, 'Internship'),
    )
    job_type = models.IntegerField(choices=job_type_choices, default=1)
    job_location_choices = (
        (1, 'Karachi'),
        (2, 'Lahore'),
        (3, 'Islamabad'),
        (4, 'Peshawar'),
        (5, 'Quetta'),
    )
    job_location = models.IntegerField(choices=job_location_choices, default=1)
    job_salary = models.IntegerField(default=0)
    job_posted_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)

    def __str__(self):
        return self.job_title


# Create your models here.
class Resume(models.Model):
    experience = models.IntegerField(default=0)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    qualification_choices = (
        ('BS', 'BS'),
        ('MS', 'MS'),
    )
    qualification = models.CharField(choices=qualification_choices, max_length=255, default='')
    job_sector_choices = (
        (1, 'Accountancy, Banking and Finance'),
        (2, 'Engineering and Manufacturing'),
        (3, 'Agriculture'),
        (4, 'Health'),
        (5, 'Property and Construction'),
        (6, 'Education'),
    )
    job_sector = models.IntegerField(choices=job_sector_choices, default=1)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    is_view = models.BooleanField(default=False)
    is_selected = models.BooleanField(default=False)
    selected_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                    related_name='selected_by')
    selected_for_job = models.ForeignKey(JobPosted, on_delete=models.CASCADE, default=None, blank=True, null=True,
                                         related_name='selected_for_job')

    def __str__(self):
        return self.user.get_full_name()

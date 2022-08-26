from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    is_job_seeker = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def get_user_type(self):
        if self.is_job_seeker:
            return 'Job Seeker'
        elif self.is_recruiter:
            return 'Recruiter'
        else:
            return 'Unknown'

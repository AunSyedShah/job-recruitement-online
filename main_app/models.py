from django.db import models
from account_app.models import User


# Create your models here.
class Resume(models.Model):
    experience = models.IntegerField(default=0)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    qualification_choices = (
        ('BS', 'BS'),
        ('MS', 'MS'),
    )
    qualification = models.CharField(choices=qualification_choices, max_length=255, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

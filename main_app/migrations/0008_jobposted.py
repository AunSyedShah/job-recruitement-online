# Generated by Django 4.1 on 2022-12-27 03:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0007_alter_resume_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPosted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=255)),
                ('job_description', models.TextField()),
                ('job_sector', models.IntegerField(choices=[(1, 'Accountancy, Banking and Finance'), (2, 'Engineering and Manufacturing'), (3, 'Agriculture'), (4, 'Health'), (5, 'Property and Construction'), (6, 'Education')], default=1)),
                ('job_type', models.IntegerField(choices=[(1, 'Full Time'), (2, 'Part Time'), (3, 'Contract'), (4, 'Internship')], default=1)),
                ('job_location', models.IntegerField(choices=[(1, 'Karachi'), (2, 'Lahore'), (3, 'Islamabad'), (4, 'Peshawar'), (5, 'Quetta')], default=1)),
                ('job_salary', models.IntegerField(default=0)),
                ('job_posted_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
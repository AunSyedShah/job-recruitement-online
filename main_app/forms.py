from .models import Resume, JobPosted
from django import forms


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        exclude = ['user', 'is_selected', 'is_view', 'selected_by', 'selected_for_job', 'selection_date']


class JobPostedForm(forms.ModelForm):
    class Meta:
        model = JobPosted
        fields = '__all__'
        exclude = ['job_posted_by']


class SearchCandidateForm(forms.ModelForm):
    class Meta:
        model = JobPosted
        fields = ('job_title',)

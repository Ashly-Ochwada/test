# workerdata/forms.py
from django import forms
from .models import Worker

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = [
            'full_name', 'national_id', 'contact_number', 'email', 'age', 
            'gender', 'marital_status', 'number_of_dependents', 'employment_type', 
            'job_role', 'employer_details', 'monthly_income', 'additional_income_sources',
            'savings_group_membership', 'existing_debts', 
            'community_references', 'guarantors', 'education_level', 'id_photo'
        ]

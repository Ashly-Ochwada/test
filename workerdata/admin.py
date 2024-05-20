# workerdata/admin.py
from django.contrib import admin
from .models import Worker, Receipt

@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_id', 'contact_number', 
                    'email', 'age', 'gender', 'marital_status', 
                    'number_of_dependents', 'employment_type', 'job_role', 
                    'employer_details', 'monthly_income', 'additional_income_sources', 
                    'savings_group_membership', 'existing_debts',  'community_references', 
                    'guarantors', 'education_level', 'id_photo')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('worker', 'receipt_type', 'file', 'upload_date')

from rest_framework import serializers
from .models import Worker, Receipt

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = [
            'id', 'full_name', 'national_id', 'contact_number', 'email', 'age', 
            'gender', 'marital_status', 'number_of_dependents', 'employment_type', 
            'job_role', 'employer_details', 'monthly_income', 'additional_income_sources',
            'savings_group_membership', 'existing_debts', 
            'community_references', 'guarantors', 'education_level', 'id_photo'
        ]

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'worker', 'receipt_type', 'file', 'upload_date']

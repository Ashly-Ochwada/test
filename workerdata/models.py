# workerdata/models.py
from django.db import models

class Worker(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    EMPLOYMENT_TYPE_CHOICES = [
        ('self_employed', 'Self Employed'),
        ('gig_worker', 'Gig Worker'),
        ('salaried', 'Salaried'),
    ]
    MONTHLY_INCOME_CHOICES = [
        ('0-5000', 'Ksh 0 - Ksh 5000'),
        ('5001-10000', 'Ksh 5001 - Ksh 10,000'),
        ('10001-20000', 'Ksh 10,001 - Ksh 20,000'),
        ('20001-30000', 'Ksh 20,001 - Ksh 30,000'),
        ('30001-40000', 'Ksh 30,001 - Ksh 40,000'),
        ('40001-50000', 'Ksh 40,001 - Ksh 50,000'),
        ('50001+', 'Above Ksh 50,000'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ]

    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=8, choices=MARITAL_STATUS_CHOICES)
    number_of_dependents = models.IntegerField()
    employment_type = models.CharField(max_length=13, choices=EMPLOYMENT_TYPE_CHOICES)
    job_role = models.CharField(max_length=100)
    employer_details = models.CharField(max_length=255, blank=True, null=True)
    monthly_income = models.CharField(max_length=11, choices=MONTHLY_INCOME_CHOICES)
    additional_income_sources = models.CharField(max_length=255, blank=True, null=True)
    savings_group_membership = models.CharField(max_length=255, blank=True, null=True)
    existing_debts = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    community_references = models.TextField(blank=True, null=True)
    guarantors = models.TextField(blank=True, null=True)
    education_level = models.CharField(max_length=255, blank=True, null=True)
    id_photo = models.ImageField(upload_to='id_photos/')

    def __str__(self):
        return self.full_name

class Receipt(models.Model):
    RECEIPT_TYPE_CHOICES = [
        ('utility_bill', 'Utility Bill'),
        ('rent_payment', 'Rent Payment'),
        ('repayment', 'Repayment'),
    ]
    worker = models.ForeignKey(Worker, related_name='receipts', on_delete=models.CASCADE)
    receipt_type = models.CharField(max_length=20, choices=RECEIPT_TYPE_CHOICES)
    file = models.FileField(upload_to='receipts/')
    upload_date = models.DateTimeField(auto_now_add=True)

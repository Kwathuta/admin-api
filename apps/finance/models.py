from django.db import models

# Create your models here.
class Approve(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount=models.DecimalField(decimal_places=2, max_digits=40)

    def __str__(self):
        return self.name

class Support(models.Model):
    message = models.TextField()  

    def __str__(self):
        return self.message    

class Payroll(models.Model):
    MPESA= 'MOBILE'
    DIRECT_DEPOSIT='BANK'
    
    PAYMENT_TYPES = (
        (MPESA, 'mobile'),
        (DIRECT_DEPOSIT, 'bank account'),
    )
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length =30)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='')
    
   
     
class Staff(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount=models.DecimalField(decimal_places=2, max_digits=40)
    position = models.CharField(max_length=100,null=True)
    full_name=models.CharField(max_length=100,null=True)
    department=models.CharField(max_length=100,null=True)
    position = models.CharField(max_length=100,null=True)
    company=models.CharField(max_length=100,null=True)
    work_email=models.CharField(max_length=100,null=True)
    personal_email=models.CharField(max_length=100,null=True)
    mobile_number=models.IntegerField(max_length=100,null=True)
    employee_id=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=100,null=True)
    date_processed=models.DateTimeField(auto_now_add=True,null=True)
    employment_date=models.DateTimeField(auto_now_add=True,null=True)
    insurance_number=models.CharField(max_length=100,null=True)
    tax_pin_number=models.CharField(max_length=100,null=True)
    paye=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    gross_pay=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    net_pay=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    tax_deducted=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    insurance=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    pension=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    sacco=models.DecimalField(decimal_places=2,max_digits=40,null=True)
    medical_cover=models.DecimalField(decimal_places=2,max_digits=40,null=True)


    def __str__(self):
        return self.name    

class Expenses(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=40)
    merchant = models.CharField(max_length=100,default='MERCHANTS')
    date_processed = models.DateTimeField(auto_now_add=True)
    approved_expenses = models.IntegerField(default='0')
    total_amount = models.DecimalField(decimal_places=2,max_digits=40,default='0')
    PENDING= 'pending'
    ACCEPTED='accepted'
    REJECTED = 'rejected'

    STATUS = (
        (PENDING, 'pending'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending')

    def __str__(self):
        return self.total_amount        
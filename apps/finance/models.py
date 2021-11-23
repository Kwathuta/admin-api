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
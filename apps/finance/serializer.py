from .models import *
from rest_framework import serializers

class ApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Approve
        fields=["id","name","created_at","updated_at","amount"]

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model=Support
        fields=["id","message"]        

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model=Staff
        fields=["id","name","created_at","updated_at","amount","postion","full_name","department","company","work_email","personal_email","employee_id",
        "location","date_processed","employment_date","insurance_number","tax_pin_number","paye","gross_pay","net_pay","tax_deducted","pension","sacco","medical_cover" ] 
class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payroll
        fields=["id","pay_id","month","debit_amount","gross_pay","net_pay","deduction","staff_paid","payroll_status"]          

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields=["id","name","merchant","date_processed","amount","status","total_amount"]
class ExpenseApprovalsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields=["id","name","amount","merchant","date"]
class ExpensePaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expenses
        fields=["id","approved_expenses","total_amount","status"]
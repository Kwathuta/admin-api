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
        fields='__all__'  
class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payroll
        fields=["id","date","full_name","payment_type"]          

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
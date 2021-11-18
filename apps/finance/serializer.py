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
        fields=["id","name","created_at","updated_at","amount","position"] 

class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payroll
        fields=["id","date","full_name","payment_type"]                             
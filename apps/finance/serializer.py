from .models import *
from rest_framework import serializers

class ApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Approve
        fields=["id","name","created_at","updated_at","amount"]
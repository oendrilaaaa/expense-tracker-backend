from rest_framework import serializers
from .models import AddTransactionModel

class AddTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTransactionModel
        fields = '__all__'
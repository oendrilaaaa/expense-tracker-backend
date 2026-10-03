from django.shortcuts import render
from rest_framework import viewsets
from .serializers import AddTransactionSerializer
from .models import AddTransactionModel

class AddTransactionViewSet(viewsets.ModelViewSet):
    queryset = AddTransactionModel.objects.all()
    serializer_class = AddTransactionSerializer
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class AddTransactionModel(models.Model):

    TRANSACTION_TYPE_CHOICES=[
        ('I','Income'),
        ('E','Expense')
    ]
    PAYMENT_METHOD_CHOICES=[
        ('Cash','Cash'),
        ('Card','Card'),
        ('UPI','UPI'),
        ('Bank','Bank')
    ]
    EXPENSE_CATEGORY_CHOICES=[
        ('Housing','Housing'),
        ('Food','Food'),
        ('Transport','Transport'),
        ('Healthcare','Healthcare'),
        ('Entertainment','Entertainment'),
        ('Utilities','Utilities'),
        ('Miscellaneous','Miscellaneous')
    ]

    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPE_CHOICES)

    description = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=12, decimal_places =2)

    date = models.DateField()

    payment_type = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    expense_category = models.CharField(max_length=20,choices=EXPENSE_CATEGORY_CHOICES)



      

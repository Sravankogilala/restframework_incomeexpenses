from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Expenses(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES','ONLINE_SERVICES'),
        ('TRAVEL','TRAVEL'),
        ('FOOD','FOOD'),
        ('RENT','RENT'),
        ('OTHERS','OTHERS'),
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS,max_length=255)
    amount = models.DecimalField(max_digits=10,decimal_places=2,max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='expenses')
    date=models.DateField(null=False,blank=False)

    def __str__(self):
        return self.category

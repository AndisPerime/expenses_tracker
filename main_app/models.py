from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Added to Budget"))

# Create your models here.


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(input_formats='%d/%m/%Y')
    category = models.CharField(max_length=50)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expenses_inputs'
        )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

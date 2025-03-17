from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Added to Budget"))
TRANSACTION_TYPE = (
    ('expense', 'Expense'),
    ('income', 'Income')
)

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#4CAF50')  # Hex color code
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='expenses'
    )
    transaction_type = models.CharField(
        max_length=7, 
        choices=TRANSACTION_TYPE,
        default='expense'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='expenses_inputs'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        transaction_symbol = '-' if self.transaction_type == 'expense' else '+'
        return f"{self.transaction_type.title()}: {self.name} ({transaction_symbol}£{self.amount}) - Added by {self.author}"

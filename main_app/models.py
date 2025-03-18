from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import calendar

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

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')], default='monthly')
    year = models.IntegerField()
    month = models.IntegerField(null=True, blank=True)
    
    def get_spent_amount(self):
        """Calculate amount spent for this budget category in the period"""
        from .models import Expense  # Import here to avoid circular import
        filter_kwargs = {
            'author': self.user,
            'category': self.category,
            'transaction_type': 'expense'
        }
        
        if self.period == 'monthly':
            filter_kwargs['date__year'] = self.year
            filter_kwargs['date__month'] = self.month
        else:  # yearly
            filter_kwargs['date__year'] = self.year
            
        spent = Expense.objects.filter(**filter_kwargs).aggregate(models.Sum('amount'))['amount__sum'] or 0
        return spent
    
    def get_remaining(self):
        """Calculate remaining amount in the budget"""
        spent = self.get_spent_amount()
        return float(self.amount) - float(spent)
    
    def get_percentage_used(self):
        """Calculate percentage of budget used"""
        if float(self.amount) == 0:
            return 100 if float(self.get_spent_amount()) > 0 else 0
            
        percentage = (float(self.get_spent_amount()) / float(self.amount)) * 100
        return min(100, round(percentage))
        
    def __str__(self):
        if self.period == 'monthly':
            return f"{self.category.name} budget for {self.month}/{self.year}"
        return f"{self.category.name} budget for {self.year}"

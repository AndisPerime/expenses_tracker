from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    date = forms.DateField(input_formats=["%d %b %Y"])

    class Meta:
        model = Expense
        fields = ['name', 'amount', 'date', 'category', 'author', 'content', 'status']

from django.shortcuts import render
from .models import Expense

# Create your views here.


def home(request):
    expenses = Expense.objects.all()
    return render(request, 'templates/home.html', {'expenses': expenses})

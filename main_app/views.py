from django.shortcuts import render
from django.http import HttpResponse
from .models import Expense

# Create your views here.


def home(request):
    expenses = Expense.objects.all()
    return render(request, 'templates/home.html', {'expenses': expenses})

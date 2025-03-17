from django.shortcuts import render
from django.views import generic
from .models import Expense

# Create your views here.


def home(request):
    expenses = Expense.objects.all()
    return render(request, 'main_app/index.html', {'expenses': expenses})

class ExpenseListView(generic.ListView):
     queryset = Expense.objects.filter(status=1).order_by('-created_at')
     template_name = 'main_app/index.html'

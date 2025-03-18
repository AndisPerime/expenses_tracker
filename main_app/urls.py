from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Remove ALL authentication-related URLs that might conflict with AllAuth
    path('update-dashboard/', views.update_dashboard, name='update_dashboard'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('get-expense/<int:expense_id>/', views.get_expense, name='get_expense'),
    path('update-expense/', views.update_expense, name='update_expense'),
    path('generate-report/', views.generate_report, name='generate_report'),
    path('add-expense/', views.add_expense, name='add_expense'),
    
    # Budget URLs - make sure they're consistent
    path('budget/', views.budget_dashboard, name='budget_dashboard'),
    path('update-budget/', views.update_budget, name='update_budget'),
    path('get-budget-data/', views.get_budget_data, name='get_budget_data'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('update-dashboard/', views.update_dashboard, name='update_dashboard'),
    path('delete-expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('get-expense/<int:expense_id>/', views.get_expense, name='get_expense'),
    path('update-expense/', views.update_expense, name='update_expense'),
    path('generate-report/', views.generate_report, name='generate_report'),
]

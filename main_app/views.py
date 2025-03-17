from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
from calendar import monthrange
from django.db.models import Sum
from django.views.decorators.http import require_POST

# Create your views here.

def home(request):
    # Ensure default categories exist
    default_categories = [
        {'name': 'Food', 'color': '#4CAF50'},
        {'name': 'Transport', 'color': '#2196F3'},
        {'name': 'Utilities', 'color': '#FFC107'},
        {'name': 'Entertainment', 'color': '#9C27B0'},
        {'name': 'Other', 'color': '#FF5722'}
    ]
    
    for cat in default_categories:
        Category.objects.get_or_create(name=cat['name'], defaults={'color': cat['color']})
    
    # For authenticated users, show their expenses only
    if request.user.is_authenticated:
        # Get current month's expenses by default
        today = datetime.today()
        first_day = datetime(today.year, today.month, 1).date()
        last_day = today.date()
        expenses = Expense.objects.filter(
            author=request.user,
            date__range=[first_day, last_day]
        ).order_by('-date')
        
        # Get summary data
        total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_count = expenses.count()
        
        # Get chart data
        chart_data = get_chart_data(request.user, first_day, last_day)
    else:
        # For anonymous users, don't show any expenses
        expenses = Expense.objects.none()
        total_amount = 0
        total_count = 0
        chart_data = {
            'labels': [],
            'data': [],
            'colors': []
        }
        
    categories = Category.objects.all()
    
    context = {
        'expenses': expenses,
        'categories': categories,
        'total_amount': total_amount,
        'total_count': total_count,
        'chart_data': chart_data
    }
    
    return render(request, 'main_app/index.html', context)


class ExpenseListView(generic.ListView):
     queryset = Expense.objects.filter(status=1).order_by('-created_at')
     template_name = 'main_app/index.html'


@login_required
def add_expense(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        date = request.POST.get('date')
      
        # Debugging output
        print(f"POST data: amount={amount}, description={description}, category_id={category_id}, date={date}")
        
        # Validate data
        if not all([amount, description, date]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Missing required fields'})
            return redirect('home')
          
        try:
            # Don't even try to use a non-numeric category ID
            if not category_id or not category_id.isdigit():
                # Just use the "Other" category directly
                print(f"Invalid category_id: {category_id}, using Other category")
                category, _ = Category.objects.get_or_create(
                    name='Other',
                    defaults={'color': '#FF5722'}
                )
            else:
                try:
                    # Use a valid numeric ID
                    category_id = int(category_id)
                    category = Category.objects.get(id=category_id)
                    print(f"Found category: {category.name} (ID: {category.id})")
                except (ValueError, Category.DoesNotExist):
                    # Fallback to Other category
                    category, _ = Category.objects.get_or_create(
                        name='Other',
                        defaults={'color': '#FF5722'}
                    )
                    print(f"Fallback to Other category (ID: {category.id})")
                
            # Create the expense with exact field names from the model
            expense = Expense.objects.create(
                name=description,
                amount=float(amount),
                date=date,
                category=category,  # This is a Category object, not an ID
                author=request.user,
                content=description,
                status=1
            )
            print(f"Created expense: {expense.name} (ID: {expense.id})")

            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'expense_id': expense.id
                })
            
            # For normal form submission
            return redirect('home')
            
        except Exception as e:
            print(f"Error creating expense: {str(e)}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': str(e)})
            # For normal form submission, redirect with an error message
            return redirect('home')
    
    # If it's a GET request, redirect to the index page
    return redirect('home')

@require_POST
@login_required
def update_dashboard(request):
    """API endpoint to update dashboard data based on date range"""
    data = json.loads(request.body)
    date_range = data.get('range', 'current-month')
    
    # Calculate start and end dates based on selected range
    today = datetime.today()
    if date_range == 'current-month':
        start_date = datetime(today.year, today.month, 1).date()
        end_date = today.date()
    elif date_range == 'last-month':
        last_month = today.month - 1 if today.month > 1 else 12
        last_month_year = today.year if today.month > 1 else today.year - 1
        _, last_day = monthrange(last_month_year, last_month)
        start_date = datetime(last_month_year, last_month, 1).date()
        end_date = datetime(last_month_year, last_month, last_day).date()
    elif date_range == 'last-3-months':
        start_date = (today - timedelta(days=90)).date()
        end_date = today.date()
    elif date_range == 'last-6-months':
        start_date = (today - timedelta(days=180)).date()
        end_date = today.date()
    elif date_range == 'year-to-date':
        start_date = datetime(today.year, 1, 1).date()
        end_date = today.date()
    elif date_range == 'custom':
        start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    else:
        # Default to current month
        start_date = datetime(today.year, today.month, 1).date()
        end_date = today.date()
    
    # Get expenses for the selected date range
    expenses = Expense.objects.filter(
        author=request.user,
        date__range=[start_date, end_date]
    ).order_by('-date')
    
    # Get summary data
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_count = expenses.count()
    
    # Get chart data
    chart_data = get_chart_data(request.user, start_date, end_date)
    
    # Format expenses for JSON response
    expense_list = []
    for expense in expenses:
        expense_list.append({
            'id': expense.id,
            'name': expense.name,
            'amount': str(expense.amount),
            'date': expense.date.strftime('%Y-%m-%d'),
            'category_name': expense.category.name if expense.category else 'Uncategorized',
            'category_color': expense.category.color if expense.category else '#777777'
        })
    
    # Return the data as JSON
    return JsonResponse({
        'total_amount': str(total_amount),
        'total_count': total_count,
        'expenses': expense_list,
        'chart_data': chart_data
    })

def get_chart_data(user, start_date, end_date):
    """Generate chart data for expense distribution by category"""
    # Get expenses grouped by category
    expenses_by_category = Expense.objects.filter(
        author=user,
        date__range=[start_date, end_date]
    ).values('category__name', 'category__color').annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')
    
    # Prepare data for chart
    labels = []
    data = []
    colors = []
    
    for item in expenses_by_category:
        category_name = item['category__name'] if item['category__name'] else 'Uncategorized'
        labels.append(category_name)
        data.append(str(item['total_amount']))
        colors.append(item['category__color'] if item['category__color'] else '#777777')
    
    return {
        'labels': labels,
        'data': data,
        'colors': colors
    }

@require_POST
@login_required
def delete_expense(request, expense_id):
    """Delete an expense"""
    try:
        expense = Expense.objects.get(id=expense_id, author=request.user)
        expense.delete()
        return JsonResponse({'success': True})
    except Expense.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Expense not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if either field is empty
        if not username or not password:
            messages.error(request, 'Please enter both username and password')
            return redirect('home')
            
        # Check if the user exists first
        try:
            user_exists = User.objects.filter(username=username).exists()
            if not user_exists:
                messages.error(request, f'No account found with username: {username}')
                return redirect('home')
        except Exception as e:
            print(f"Error checking user existence: {str(e)}")
            
        # Try to authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return redirect('home')
    
    # For GET requests, just redirect to home page which has the login form
    return redirect('home')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('home')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('home')
        
        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Log the user in
        login(request, user)
        return redirect('home')
    
    # For GET requests, just redirect to home page which has the register form
    return redirect('home')

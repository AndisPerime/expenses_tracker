from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Expense, Category, Budget
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime, timedelta
from calendar import monthrange
from django.db.models import Sum  # We can use this instead of models.Sum
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
import calendar


# Create your views here.
from .forms import CustomUserCreationForm, CustomAuthenticationForm


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
        Category.objects.get_or_create(
            name=cat['name'],
            defaults={'color': cat['color']}
        )

    # For authenticated users, show their expenses only
    if request.user.is_authenticated:
        # Get current month's expenses by default
        today = datetime.today()
        first_day = datetime(today.year, today.month, 1).date()
        last_day = today.date()
        transactions = Expense.objects.filter(
            author=request.user,
            date__range=[first_day, last_day]
        ).order_by('-date')

        # Separate expenses and income
        expenses = transactions.filter(transaction_type='expense')
        income = transactions.filter(transaction_type='income')

        # Make sure Income category exists
        income_category, _ = Category.objects.get_or_create(
            name='Income',
            defaults={'color': '#4CAF50'}  # Green color for income
        )

        # Get categories excluding Income category for the dropdown
        display_categories = Category.objects.exclude(name='Income')

        # Get summary data
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
        net_amount = float(total_income) - float(total_expenses)

        # Format to two decimal places
        total_expenses = round(float(total_expenses), 2)
        total_income = round(float(total_income), 2)
        net_amount = round(net_amount, 2)
        total_count = transactions.count()

        # Get chart data
        chart_data = get_chart_data(request.user, first_day, last_day)
    else:
        # For anonymous users, don't show any expenses
        transactions = Expense.objects.none()
        total_income = 0
        total_expenses = 0
        net_amount = 0
        total_count = 0
        chart_data = {
            'labels': [],
            'data': [],
            'colors': []
        }
        display_categories = Category.objects.none()

    context = {
        'expenses': transactions,
        'categories': display_categories,  # Use filtered categories
        'total_amount': total_expenses,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_amount': net_amount,
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
        date = request.POST.get('date')
        transaction_type = request.POST.get(
            'transaction_type', 'expense')  # Default to expense

        # Get or create the Income category for income transactions
        if transaction_type == 'income':
            category, _ = Category.objects.get_or_create(
                name='Income',
                defaults={'color': '#4CAF50'}  # Green color for income
            )
        else:
            # For expenses, process the category as before
            category_id = request.POST.get('category')

            # Don't try to use 'income' as a category ID
            if category_id == 'income':
                category, _ = Category.objects.get_or_create(
                    name='Other',
                    defaults={'color': '#FF5722'}
                )
            elif not category_id or not category_id.isdigit():
                # Fallback to Other category
                category, _ = Category.objects.get_or_create(
                    name='Other',
                    defaults={'color': '#FF5722'}
                )
            else:
                try:
                    # Use a valid numeric ID
                    category_id = int(category_id)
                    category = Category.objects.get(id=category_id)
                except (ValueError, Category.DoesNotExist):
                    # Fallback to Other category
                    category, _ = Category.objects.get_or_create(
                        name='Other',
                        defaults={'color': '#FF5722'}
                    )

        # Validate required data
        if not all([amount, description, date]):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False,
                                     'error': 'Missing required fields'})
            return redirect('home')

        try:
            # Create the expense/income transaction
            expense = Expense.objects.create(
                name=description,
                amount=float(amount),
                date=date,
                category=category,
                transaction_type=transaction_type,
                author=request.user,
                content=description,
                status=1
            )
            print(f"Created {transaction_type}: {
                expense.name} (ID: {expense.id})")

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
        start_date = datetime.strptime(data.get
                                       ('start_date'), '%Y-%m-%d').date()
        end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    else:
        # Default to current month
        start_date = datetime(today.year, today.month, 1).date()
        end_date = today.date()

    # Get expenses for the selected date range
    transactions = Expense.objects.filter(
        author=request.user,
        date__range=[start_date, end_date]
    )

    # Separate expenses and income
    expenses = transactions.filter(transaction_type='expense')
    income = transactions.filter(transaction_type='income')

    # Get summary data
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
    net_amount = float(total_income) - float(total_expenses)

    total_expenses = round(float(total_expenses), 2)
    total_income = round(float(total_income), 2)
    net_amount = round(net_amount, 2)
    total_count = transactions.count()

    # Get chart data
    chart_data = get_chart_data(request.user, start_date, end_date)
    chart_data['total_income'] = total_income
    chart_data['total_expenses'] = total_expenses
    chart_data['net_amount'] = net_amount

    # Format transactions for JSON response
    transaction_list = []
    for transaction in transactions.order_by('-date'):
        transaction_list.append({
            'id': transaction.id,
            'name': transaction.name,
            'amount': f"{float(transaction.amount):.2f}",
            'date': transaction.date.strftime('%Y-%m-%d'),
            'category_name': transaction.category.name
            if transaction.category else 'Uncategorized',
            'category_color': transaction.category.color
            if transaction.category else '#777777',
            'transaction_type': transaction.transaction_type
        })

    # Return the data as JSON
    return JsonResponse({
        # Changed to return net_amount for total
        'total_amount': f"{net_amount:.2f}",
        'total_expenses': f"{total_expenses:.2f}",
        'total_income': f"{total_income:.2f}",
        'net_amount': f"{net_amount:.2f}",
        'total_count': total_count,
        'expenses': transaction_list,
        'chart_data': chart_data
    })


@login_required
def get_expense(request, expense_id):
    """Get expense data for editing"""
    try:
        expense = Expense.objects.get(id=expense_id, author=request.user)
        expense_data = {
            'id': expense.id,
            'name': expense.name,
            'amount': float(expense.amount),
            'date': expense.date.strftime('%Y-%m-%d'),
            'category_id': expense.category.id if expense.category else '',
            'transaction_type': expense.transaction_type
        }
        return JsonResponse({'success': True, 'expense': expense_data})
    except Expense.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Expense not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
@require_http_methods(["POST"])
def update_expense(request):
    """Update an existing expense"""
    try:
        expense_id = request.POST.get('expense_id')
        if not expense_id:
            return JsonResponse({'success': False,
                                 'error': 'No expense ID provided'})

        expense = Expense.objects.get(id=expense_id, author=request.user)

        # Update fields
        expense.name = request.POST.get('description', expense.name)
        expense.amount = float(request.POST.get('amount', expense.amount))
        expense.date = request.POST.get('date', expense.date)
        expense.transaction_type = request.POST.get(
            'transaction_type', expense.transaction_type)

        # Handle category based on transaction type
        if expense.transaction_type == 'income':
            category, _ = Category.objects.get_or_create(
                name='Income',
                defaults={'color': '#4CAF50'}
            )
            expense.category = category
        else:
            category_id = request.POST.get('category')
            if category_id and category_id.isdigit():
                try:
                    category = Category.objects.get(id=int(category_id))
                    expense.category = category
                except Category.DoesNotExist:
                    # Keep existing category if invalid
                    pass

        expense.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True})

        return redirect('home')

    except Expense.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Expense not found'})
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})
        return redirect('home')


def get_chart_data(user, start_date, end_date):
    """Generate chart data for expense distribution by category"""
    # Get expenses grouped by category (only expenses, not income)
    expenses_by_category = Expense.objects.filter(
        author=user,
        date__range=[start_date, end_date],
        transaction_type='expense'  # Only include expenses in the pie chart
    ).values('category__name', 'category__color').annotate(
        total_amount=Sum('amount')
    ).order_by('-total_amount')

    # Prepare data for chart
    labels = []
    data = []
    colors = []

    # Check if there are any expenses
    if not expenses_by_category:
        return {
            'labels': ['No expenses'],
            'data': [0],
            'colors': ['#cccccc']
        }

    for item in expenses_by_category:
        category_name = item[
            'category__name'
            ] if item['category__name'] else 'Uncategorized'
        labels.append(category_name)
        # Format to 2 decimal places
        data.append(f"{float(item['total_amount']):.2f}")
        colors.append(item[
            'category__color'
            ] if item['category__color'] else '#777777')

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

# Remove or comment out the login and
# register functions to avoid conflicts with AllAuth


"""
def user_login(request):
    # This function conflicts with allauth's login
    # ...existing code...
    pass

def register(request):
    # This function conflicts with allauth's signup
    # ...existing code...
    pass
"""


# Keep the logout function but redirect to allauth's logout
def user_logout(request):
    logout(request)
    return redirect('account_logout')


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

        # Log the user in with explicit backend
        login(
            request, user, backend='django.contrib.auth.backends.ModelBackend'
              )
        return redirect('home')

    # For GET requests, just redirect to home page which has the register form
    return redirect('home')


@login_required
def generate_report(request):
    """Generate an HTML report for a time period"""
    if request.method == 'POST':
        title = request.POST.get('title', 'Financial Report')
        period = request.POST.get('period', 'current-month')

        # Get the date range
        start_date, end_date = get_date_range_from_period(period, request)

        # Get expense data for the period
        transactions = Expense.objects.filter(
            author=request.user,
            date__range=[start_date, end_date]
        ).order_by('-date')

        # Separate expenses and income
        expenses = transactions.filter(transaction_type='expense')
        income = transactions.filter(transaction_type='income')

        # Calculate summaries
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        total_income = income.aggregate(Sum('amount'))['amount__sum'] or 0
        net_amount = float(total_income) - float(total_expenses)

        # Format to two decimal places
        total_expenses = round(float(total_expenses), 2)
        total_income = round(float(total_income), 2)
        net_amount = round(net_amount, 2)

        # Get include options
        include_summary = request.POST.get('include_summary') == 'on'
        include_charts = request.POST.get('include_charts') == 'on'
        include_transactions = request.POST.get('include_transactions') == 'on'

        # Prepare chart data
        chart_data = None
        if include_charts:
            chart_data = get_chart_data(request.user, start_date, end_date)

        # Prepare context for template
        context = {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'transactions': transactions,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_amount': net_amount,
            'transaction_count': transactions.count(),
            'include_summary': include_summary,
            'include_charts': include_charts,
            'include_transactions': include_transactions,
            'chart_data': chart_data,
            'generated_at': datetime.now(),
            'user': request.user,
        }

        # Return HTML report
        return render(request, 'main_app/report.html', context)

    # Redirect to home if not POST
    return redirect('home')


def get_date_range_from_period(period, request):
    """Convert a period name to start and end dates"""
    today = datetime.today()

    if period == 'current-month':
        start_date = datetime(today.year, today.month, 1).date()
        end_date = today.date()
    elif period == 'last-month':
        last_month = today.month - 1 if today.month > 1 else 12
        last_month_year = today.year if today.month > 1 else today.year - 1
        _, last_day = monthrange(last_month_year, last_month)
        start_date = datetime(last_month_year, last_month, 1).date()
        end_date = datetime(last_month_year, last_month, last_day).date()
    elif period == 'last-3-months':
        start_date = (today - timedelta(days=90)).date()
        end_date = today.date()
    elif period == 'last-6-months':
        start_date = (today - timedelta(days=180)).date()
        end_date = today.date()
    elif period == 'year-to-date':
        start_date = datetime(today.year, 1, 1).date()
        end_date = today.date()
    elif period == 'custom':
        try:
            start_date = datetime.strptime(request.POST.get(
                'start_date'
                ), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.POST.get(
                'end_date'
                ), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            # Default to current month if dates are invalid
            start_date = datetime(today.year, today.month, 1).date()
            end_date = today.date()
    else:
        # Default to current month
        start_date = datetime(today.year, today.month, 1).date()
        end_date = today.date()

    return start_date, end_date


@login_required
def budget_dashboard(request):
    """Budget management dashboard view"""
    # Get current year and month
    today = timezone.now()
    current_year = today.year
    current_month = today.month

    # Get categories for the user
    categories = Category.objects.exclude(name='Income')

    # Get user's budgets
    monthly_budgets = Budget.objects.filter(
        user=request.user,
        period='monthly',
        year=current_year,
        month=current_month
    ).select_related('category')

    # Get yearly budgets (removed unused variable)

    # Get all expenses for current month to calculate spending
    month_expenses = Expense.objects.filter(
        author=request.user,
        date__year=current_year,
        date__month=current_month,
        transaction_type='expense'
    )

    # Get total budget and spending
    total_monthly_budget = sum([float(b.amount) for b in monthly_budgets])
    total_monthly_spent = sum(
        [float(b.get_spent_amount()) for b in monthly_budgets]
        )

    # Budget data for each category
    budget_data = []
    for category in categories:
        # Try to get existing budget for this category
        try:
            monthly_budget = monthly_budgets.get(category=category)
            amount = float(monthly_budget.amount)
            spent = float(monthly_budget.get_spent_amount())
            remaining = float(monthly_budget.get_remaining())
            percentage = monthly_budget.get_percentage_used()
        except Budget.DoesNotExist:
            # No budget exists for this category
            amount = 0
            spent = float(month_expenses.filter(
                category=category
                ).aggregate(Sum('amount'))['amount__sum'] or 0)
            remaining = -spent
            percentage = 100 if amount == 0 and spent > 0 else 0

        budget_data.append({
            'category': category,
            'amount': amount,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage
        })

    # Calculate percentage of month passed
    _, last_day = calendar.monthrange(current_year, current_month)
    days_in_month = last_day
    days_passed = min(today.day, days_in_month)
    month_progress = round((days_passed / days_in_month) * 100)

    context = {
        'budget_data': budget_data,
        'total_budget': total_monthly_budget,
        'total_spent': total_monthly_spent,
        'month': calendar.month_name[current_month],
        'year': current_year,
        'current_month': current_month,  # Add the month number to the context
        'categories': categories,
        'month_progress': month_progress
    }

    return render(request, 'main_app/budget.html', context)


@require_POST
@login_required
def update_budget(request):
    """API endpoint to create or update a budget"""
    category_id = request.POST.get('category_id')
    amount = request.POST.get('amount')
    period = request.POST.get('period', 'monthly')

    # Add defensive checks for year and month
    try:
        year = int(request.POST.get('year', timezone.now().year))
    except (ValueError, TypeError):
        year = timezone.now().year

    # For month, handle it differently based on period
    if period == 'monthly':
        try:
            month_value = request.POST.get('month')
            month = int(month_value) if month_value and month_value.strip(

            ) else timezone.now().month
        except (ValueError, TypeError):
            month = timezone.now().month
    else:
        month = None

    # Validate data
    if not all([category_id, amount]) or float(amount) < 0:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False,
                                 'error': 'Invalid budget data'})
        messages.error(request, 'Invalid budget data')
        return redirect('budget_dashboard')

    try:
        category = Category.objects.get(id=category_id)
        # Get or create budget
        budget, created = Budget.objects.update_or_create(
            user=request.user,
            category=category,
            period=period,
            year=year,
            month=month if period == 'monthly' else None,
            defaults={'amount': amount}
        )

        # Return success
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'budget_id': budget.id,
                'message': 'Budget updated successfully'
            })

        messages.success(request, f'{period.capitalize()} budget for {
            category.name
            } updated successfully')
        return redirect('budget_dashboard')

    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': str(e)})

        messages.error(request, f'Error updating budget: {str(e)}')
        return redirect('budget_dashboard')


@require_POST
@login_required
def get_budget_data(request):
    """Get budget vs. spending data for visualizations"""
    data = json.loads(request.body)
    year = data.get('year', timezone.now().year)
    month = data.get('month', timezone.now().month)

    # Get all categories
    categories = Category.objects.exclude(name='Income')

    # Prepare data for chart
    labels = []
    budget_amounts = []
    spent_amounts = []
    colors = []

    for category in categories:
        # Try to get budget for category
        try:
            budget = Budget.objects.get(
                user=request.user,
                category=category,
                period='monthly',
                year=year,
                month=month
            )
            budget_amount = float(budget.amount)
        except Budget.DoesNotExist:
            budget_amount = 0

        # Get actual spending
        spent = Expense.objects.filter(
            author=request.user,
            category=category,
            date__year=year,
            date__month=month,
            transaction_type='expense'
        ).aggregate(Sum('amount'))[
            'amount__sum'
            ] or 0  # Use Sum instead of models.Sum

        labels.append(category.name)
        budget_amounts.append(budget_amount)
        spent_amounts.append(float(spent))
        colors.append(category.color)

    return JsonResponse({
        'success': True,
        'labels': labels,
        'budget_amounts': budget_amounts,
        'spent_amounts': spent_amounts,
        'colors': colors
    })


def budget_view(request):
    """View function for the budget dashboard."""
    # Simply redirect to the budget_dashboard view
    return budget_dashboard(request)


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print(f"Form data: {request.POST}")
        print(f"Form is valid: {form.is_valid()}")
        if form.is_valid():
            user = form.save()
            # Explicitly specify the backend when logging in
            login(request, user, backend='django.contrib'
                  '.auth.backends.ModelBackend')
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            print(f"Form errors: {form.errors}")
            messages.error(
                request, "Error creating account. Please check the form."
                )
    else:
        form = CustomUserCreationForm()
    return render(request, 'main_app/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        print(f"Login form data: {request.POST}")
        print(f"Login form is valid: {form.is_valid()}")
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(f"User authenticated: {user is not None}")
            if user is not None:
                # The authenticate function returns a user with backend set
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')
            else:
                print("Authentication failed despite valid form")
        else:
            print(f"Login form errors: {form.errors}")
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    return render(request, 'main_app/login.html', {'form': form})

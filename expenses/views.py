from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Budget, Expense, Category
from .forms import BudgetForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


# Add home view function
def home(request):
    return render(request, 'expenses/home.html')


@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    context = {
        'budgets': budgets
    }
    return render(request, 'expenses/budget_list.html', context)


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'expenses/budget_form.html', context)


@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(request.user, instance=budget)

    context = {
        'form': form,
        'budget': budget
    }
    return render(request, 'expenses/budget_form.html', context)


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budget_list')
    return render(
        request, 'expenses/budget_confirm_delete.html', {'budget': budget}
        )


@login_required
def budget_dashboard(request):
    # Get current month budgets
    current_month = timezone.now().month
    current_year = timezone.now().year

    # Get monthly budgets
    budgets = Budget.objects.filter(
        user=request.user,
        period='monthly',
        start_date__month__lte=current_month,
        start_date__year__lte=current_year
    )

    budget_data = []

    for budget in budgets:
        # Calculate actual spending for this category in current month
        actual_spending = Expense.objects.filter(
            user=request.user,
            category=budget.category,
            date__month=current_month,
            date__year=current_year
        ).aggregate(total=Sum('amount'))['total'] or 0

        # Calculate percentage spent
        percentage = (float(actual_spending) / float(
            budget.amount
            )) * 100 if float(budget.amount) > 0 else 0
        percentage = min(percentage, 100)  # Cap at 100% for visualization

        budget_data.append({
            'category': budget.category.name,
            'budget_amount': float(budget.amount),
            'actual_spending': float(actual_spending),
            'percentage': percentage,
            'remaining': float(budget.amount) - float(actual_spending),
            'color': 'green' if percentage < 80 else (
                'orange' if percentage < 100 else 'red'
                )
        })

    context = {
        'budget_data': budget_data
    }
    return render(request, 'expenses/budget_dashboard.html', context)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'expenses/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'expenses/category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    template_name = 'expenses/category_form.html'
    fields = ['name']
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'expenses/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

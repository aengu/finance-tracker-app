from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .filters import TransactionFilter
from .forms import TransactionForm

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        'filter' : transaction_filter,
        'total_income' : total_income,
        'total_expenses': total_expenses,
        'net_income':total_income - total_expenses
        }

    # htmx 요청이 있는 경우, 템플릿의 일부분만 반환 
    if request.htmx:
        return render(request, 'tracker/partials/transaction-container.html', context)
    
    return render(request, 'tracker/transaction-list.html', context)

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'msg': '성공적으로 추가 되었습니다.'}

            return render(request, 'tracker/partials/transaction-success.html', context)
    context = {'form': TransactionForm()}
    return render(request, 'tracker/partials/create-transaction.html', context)
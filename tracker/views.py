from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .filters import TransactionFilter

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    # transactions = Transaction.objects.filter(user = request.user)
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    context = {'filter' : transaction_filter}

    # htmx 요청이 있는 경우, 템플릿의 일부분만 반환 
    if request.htmx:
        return render(request, 'tracker/particials/transaction-container.html', context)
    
    return render(request, 'tracker/transaction-list.html', context)
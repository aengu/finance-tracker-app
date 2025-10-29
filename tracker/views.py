from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django_htmx.http import retarget
from django.core.paginator import Paginator
from django.conf import settings
from .models import Transaction, Category
from .filters import TransactionFilter
from .forms import TransactionForm
from .charting import plot_income_expenses_bar_chart, plot_category_pie_chart

# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')

@login_required
def transaction_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    page = int(request.GET.get('page', 1))

    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(page)
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
        'transactions': transaction_page, 
        'filter' : transaction_filter,
        'total_income' : total_income,
        'total_expenses': total_expenses,
        'net_income':total_income - total_expenses
        }

    # htmx 요청이 있는 경우, 템플릿의 일부분만 반환 
    if request.htmx:
        if page > 1: # 무한스크롤 요청인 경우
            return render(request, 'tracker/partials/transaction-container.html#transaction-partial', context)
        return render(request, 'tracker/partials/transaction-container.html', context)
    
    return render(request, 'tracker/transaction-list.html', context)


"""
* django-htmx의 retarget(response, target)
- htmx가 응답을 삽입할 대상 요소를 서버에서 동적으로 변경할 수 있게 함
- 실제로 요청 헤더에 'HX-Retarget' : target 이렇게 설정됨
- 주로 form의 유효성 검사나, 부분 UI 갱신에 사용된다.
"""

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = {'msg': '성공적으로 추가 되었습니다.'}

            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form}
            response =  render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')
    context = {'form': TransactionForm()}
    return render(request, 'tracker/partials/create-transaction.html', context)


@login_required
def update_transaction(request, pk:int):

    # 별 거 아니지만 이런 update 요청 받을 때 user=request.user인지도 꼭 확인해야 한다.
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.save()
            context = {'msg': '성공적으로 수정 되었습니다.'}

            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = {'form': form, 'transction': transaction}
            response =  render(request, 'tracker/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')
    context = {'form': TransactionForm(instance=transaction), 'transaction':transaction}
    return render(request, 'tracker/partials/update-transaction.html', context)

@login_required
@require_http_methods(["DELETE"]) # 명시된 http 메서드만 허용하는 데코레이터
def delete_transaction(request, pk:int):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = {'msg': f"{transaction.date}일자의 {transaction.amount}원 거래내역이 성공적으로 삭제 되었습니다."}
    return render(request, 'tracker/partials/transaction-success.html', context)


@login_required 
def transaction_charts(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    bar_chart = plot_income_expenses_bar_chart(transaction_filter.qs)
    income_pie_chart = plot_category_pie_chart(transaction_filter.qs.filter(type='income'), '카테고리별 수익합계')
    expense_pie_chart = plot_category_pie_chart(transaction_filter.qs.filter(type='expense'), '카테고리별 지출합계')

    context = {
        'filter': transaction_filter,
        'income_expense_bar_chart':bar_chart.to_html(full_html=False),
        'income_pie_chart': income_pie_chart.to_html(full_html=False),
        'expense_pie_chart': expense_pie_chart.to_html(full_html=False),
    }
    # htmx요청인 경우 컨테이너부분만 로드
    if request.htmx:
        return render(request, 'tracker/partials/charts-container.html', context)
    
    return render(request, 'tracker/charts.html', context)
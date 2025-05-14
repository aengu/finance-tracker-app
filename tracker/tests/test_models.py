import pytest
from tracker.models import Transaction

'''
기본적으로 pytest는 django db에 접근을 못함
그래서 pytest-django 패키지를 통해 pytest 메서드가 django test db에 접근할 수 있게 한다
이 경우 conftest에서 만든 transaction 더미 데이터에 접근하기 위해 데코레이터를 사용함
'''
@pytest.mark.django_db
def test_queryset_get_income_method(transactions):
    qs = Transaction.objects.get_income()
    assert qs.count() > 0
    assert all (
        [transaction.type == 'income' for transaction in qs]
    )

@pytest.mark.django_db
def test_queryset_get_expenses_method(transactions):
    qs = Transaction.objects.get_expense()
    assert qs.count() > 0
    assert all (
        [transaction.type == 'expense' for transaction in qs]
    )

@pytest.mark.django_db
def test_queryset_get_total_income_method(transactions):
    total_income = Transaction.objects.get_total_income()
    assert total_income == sum(t.amount for t in transactions if t.type == 'income')

@pytest.mark.django_db
def test_queryset_get_total_expenses_method(transactions):
    total_expenses = Transaction.objects.get_total_expenses()
    assert total_expenses == sum(t.amount for t in transactions if t.type == 'expense')
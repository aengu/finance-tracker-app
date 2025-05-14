import pytest
from django.urls import reverse

@pytest.fixture
def test_total_values_appear_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == 'income')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
    net = income_total - expense_total

    response = client.get(reverse('transaction_list'))
    assert response.conetxt['total_income'] == income_total
    assert response.conetxt['total_expenses'] == expense_total
    assert response.conetxt['net_income'] == net
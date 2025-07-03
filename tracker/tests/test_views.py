from datetime import datetime, timedelta
import pytest
from django.urls import reverse
from tracker.tests.decorators import query_debugger
from tracker.models import Category, Transaction
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client):
    """transaction-list페이지에 총합의 값이 알맞게 나오는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == 'income')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
    net = income_total - expense_total

    response = client.get(reverse('transaction-list'))
    assert response.context['total_income'] == income_total
    assert response.context['total_expenses'] == expense_total
    assert response.context['net_income'] == net

@pytest.mark.django_db
@query_debugger
def test_transaction_type_filter1(user_transactions, client):
    """transaction-list페이지의 type필터가 제대로 동작하는지 테스트. qs를 순회하며 type을 확인"""
    user = user_transactions[0].user
    client.force_login(user)

    # income check
    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs
    # print(qs._result_cache)
    for tr in qs:
        assert tr.type == 'income'

    # expense check
    GET_params = {'transaction_type': 'expense'}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs
    for tr in qs:
        assert tr.type == 'expense'


@pytest.mark.django_db
@query_debugger
def test_transaction_type_filter2(user_transactions, client):
    """transaction-list페이지의 타입 필터가 제대로 동작하는지 테스트. exists()를 이용하여 qs의 type들을 한 번에 확인"""
    user = user_transactions[0].user
    client.force_login(user)

    # income check
    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs
    assert not qs.filter(type='expense').exists()

    # expense check
    GET_params = {'transaction_type': 'expense'}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs
    assert not qs.filter(type='income').exists()

@pytest.mark.django_db
def test_start_end_date_filter(user_transactions, client):
    """transaction-list페이지의 날짜 필터가 제대로 동작하는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    # start date check
    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date >= start_date_cutoff

    # end date check
    end_date_cutoff = datetime.now().date() + timedelta(days=120)
    GET_params = {'end_date': end_date_cutoff}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date <= end_date_cutoff

@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    """transaction-list페이지의 카테고리 필터가 제대로 동작하는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    # 첫 번째, 두 번째 category pk 가져오기
    category_pks = Category.objects.all()[:2].values_list('pk', flat=True)
    GET_params = {'category': category_pks}
    response = client.get(reverse('transaction-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.category.pk in category_pks

@pytest.mark.django_db
def test_add_transaction_request(user, transaction_dict_params, client):
    """ """
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    # send request with transction data
    headers = {'HTTP_HX-Request': 'true'}
    response = client.post(
        reverse('create-transaction'),
        transaction_dict_params,
        **headers
    )

    # POST요청 이후 객체의 갯수가 1개 증가했는지 확인
    assert Transaction.objects.filter(user=user).count() == user_transaction_count + 1
    # form의 유효성 검사가 통과되어 알맞은 템플릿을 반환했는지 확인
    assertTemplateUsed(response, 'tracker/partials/transaction-success.html')

@pytest.mark.django_db
def test_cannot_add_transaction_with_nagative_amount(
    user,
    transaction_dict_params,
    client):
    """ """
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    transaction_dict_params['amount'] = -5
    response = client.post( # 사실 여기선 request에 htmx header를 안 넣어도 통과되긴 한다
        reverse('create-transaction'),
        transaction_dict_params,
    )

    # POST요청 이후 객체의 갯수가 그대로인지 확인
    assert Transaction.objects.filter(user=user).count() == user_transaction_count
    # form의 유효성 검사가 통과되지 않아 알맞은 템플릿을 반환했는지 확인
    assertTemplateUsed(response, 'tracker/partials/create-transaction.html')
    # 응답의 헤더에 retarget속성이 설정되어 있는지 확인
    assert 'HX-Retarget' in response.headers

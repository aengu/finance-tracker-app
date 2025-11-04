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
    """트랜잭션 추가 기능 테스트. 생성요청 전 후로 전체 트랜잭션 갯수 비교"""
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
    """amount에 음수를 넣고 생성 요청 후, 전체 트랜잭션 갯수의 변화가 없는지 확인"""
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

@pytest.mark.django_db
def test_update_transaction_request(user, transaction_dict_params, client):
    """거래내역 수정 메서드 동작 확인"""
    client.force_login(user)
    # transaction_dict_params fixture를 선언하면서 인스턴스 하나 만들었음
    assert Transaction.objects.filter(user = user).count() == 1

    transaction = Transaction.objects.first()
    now = datetime.now().date()
    # dict params을 수정하여 post 요청으로 트랜잭션을 수정
    transaction_dict_params['amount'] = 99999
    transaction_dict_params['date'] = now
    response = client.post(
        reverse('update-transaction', kwargs={'pk': transaction.id}),
        transaction_dict_params,
    )

    # 요청이 업데이트 되었는지 확인하고 새로운 트랜잭션이 생성되지 않았는지 확인
    assert Transaction.objects.filter(user = user).count() == 1
    assert Transaction.objects.first().amount == 99999
    assert Transaction.objects.first().date == now

@pytest.mark.django_db
def test_delete_transaction_request(user, transaction_dict_params, client):
    """거래내역 삭제 메서드 동작 확인"""
    client.force_login(user)

    assert Transaction.objects.filter(user = user).count() == 1
    transaction = Transaction.objects.first()
    response = client.delete(
        reverse('delete-transaction', kwargs={'pk': transaction.id})
    )
    assert Transaction.objects.filter(user = user).count() == 0

@pytest.mark.django_db
def test_transaction_charts_page_requires_login(client):
    """차트 페이지에 로그인 없이 접근 시 리다이렉트되는지 테스트"""
    response = client.get(reverse('transaction-charts'))
    # 로그인 페이지로 리다이렉트되어야 함
    assert response.status_code == 302
    assert '/accounts/login/' in response.url

@pytest.mark.django_db
def test_transaction_charts_page_access(user_transactions, client):
    """로그인 후 차트 페이지에 정상 접근되는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    response = client.get(reverse('transaction-charts'))

    assert response.status_code == 200
    assertTemplateUsed(response, 'tracker/charts.html')

@pytest.mark.django_db
def test_transaction_charts_page_contains_all_charts(user_transactions, client):
    """차트 페이지에 3개의 차트가 모두 포함되어 있는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    response = client.get(reverse('transaction-charts'))

    # context에 3개의 차트가 모두 있고 값이 존재하는지 확인
    assert 'income_expense_bar_chart' in response.context
    assert response.context['income_expense_bar_chart']
    assert 'income_pie_chart' in response.context
    assert response.context['income_pie_chart']
    assert 'expense_pie_chart' in response.context
    assert response.context['expense_pie_chart']

@pytest.mark.django_db
def test_transaction_charts_page_with_filter(user_transactions, client):
    """차트 페이지에 필터가 적용되는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    # income 타입만 필터링
    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('transaction-charts'), GET_params)

    assert response.status_code == 200
    # 필터가 context에 포함되어 있는지 확인
    assert 'filter' in response.context
    # 필터된 queryset이 income만 포함하는지 확인
    qs = response.context['filter'].qs
    assert not qs.filter(type='expense').exists()

@pytest.mark.django_db
def test_transaction_charts_htmx_request(user_transactions, client):
    """htmx 요청 시 부분 템플릿만 반환되는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    headers = {'HTTP_HX-Request': 'true'}
    response = client.get(reverse('transaction-charts'), **headers)

    assert response.status_code == 200
    # htmx 요청 시 부분 템플릿이 사용되는지 확인
    assertTemplateUsed(response, 'tracker/partials/charts-container.html')

@pytest.mark.django_db
def test_transaction_charts_page_shows_user_data_only(client):
    """차트 페이지가 현재 로그인한 사용자의 데이터만 표시하는지 테스트"""
    from tracker.factories import UserFactory, TransactionFactory

    # 두 명의 사용자 생성
    user1 = UserFactory()
    user2 = UserFactory()

    # 각 사용자의 거래 생성
    user1_transactions = TransactionFactory.create_batch(10, user=user1)
    user2_transactions = TransactionFactory.create_batch(10, user=user2)

    # user1로 로그인
    client.force_login(user1)
    response = client.get(reverse('transaction-charts'))

    # user1의 데이터만 필터링되었는지 확인
    qs = response.context['filter'].qs
    assert qs.count() == 10
    assert all(t.user == user1 for t in qs)

@pytest.mark.django_db
def test_transaction_charts_with_date_filter(user_transactions, client):
    """차트 페이지에 날짜 필터가 적용되는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    # 120일 전부터의 거래만 필터링
    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('transaction-charts'), GET_params)

    assert response.status_code == 200
    qs = response.context['filter'].qs

    # 필터링된 모든 거래가 start_date 이후인지 확인
    for transaction in qs:
        assert transaction.date >= start_date_cutoff

@pytest.mark.django_db
def test_transaction_charts_with_category_filter(user_transactions, client):
    """차트 페이지에 카테고리 필터가 적용되는지 테스트"""
    user = user_transactions[0].user
    client.force_login(user)

    # 첫 번째 카테고리로 필터링
    category_pk = Category.objects.first().pk
    GET_params = {'category': [category_pk]}
    response = client.get(reverse('transaction-charts'), GET_params)

    assert response.status_code == 200
    qs = response.context['filter'].qs

    # 필터링된 모든 거래가 해당 카테고리에 속하는지 확인
    for transaction in qs:
        assert transaction.category.pk == category_pk

@pytest.mark.django_db
def test_transaction_charts_with_no_data(user, client):
    """거래 데이터가 없을 때 차트 페이지가 정상 작동하는지 테스트"""
    client.force_login(user)

    response = client.get(reverse('transaction-charts'))

    # 데이터가 없어도 페이지는 정상적으로 렌더링되어야 함
    assert response.status_code == 200
    assert 'income_expense_bar_chart' in response.context
    assert response.context['income_expense_bar_chart']
    assert 'income_pie_chart' in response.context
    assert response.context['income_pie_chart']
    assert 'expense_pie_chart' in response.context
    assert response.context['expense_pie_chart']

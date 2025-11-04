import pytest
from tracker.models import Transaction, Category
from tracker.charting import plot_income_expenses_bar_chart, plot_category_pie_chart
import plotly.graph_objects as go


@pytest.mark.django_db
def test_plot_income_expenses_bar_chart_returns_figure(user_transactions):
    """총수입/총지출 막대 차트가 정상적으로 생성되는지 테스트"""
    user = user_transactions[0].user
    qs = Transaction.objects.filter(user=user)

    fig = plot_income_expenses_bar_chart(qs)

    # plotly Figure 객체가 반환되는지 확인
    assert isinstance(fig, go.Figure)
    # 차트에 데이터가 있는지 확인
    assert len(fig.data) > 0
    # x축에 '총수입', '총지출'이 있는지 확인
    assert fig.data[0].x is not None


@pytest.mark.django_db
def test_plot_income_expenses_bar_chart_correct_values(user_transactions):
    """막대 차트의 값이 실제 수입/지출 합계와 일치하는지 테스트"""
    user = user_transactions[0].user
    qs = Transaction.objects.filter(user=user)

    # 실제 총수입과 총지출 계산
    total_income = sum(t.amount for t in user_transactions if t.type == 'income')
    total_expense = sum(t.amount for t in user_transactions if t.type == 'expense')

    fig = plot_income_expenses_bar_chart(qs)

    # 차트의 y값이 실제 합계와 일치하는지 확인
    chart_values = fig.data[0].y
    assert chart_values[0] == total_income
    assert chart_values[1] == total_expense


@pytest.mark.django_db
def test_plot_income_expenses_bar_chart_with_empty_queryset(user):
    """빈 queryset으로 막대 차트 생성 시 오류 없이 처리되는지 테스트"""
    qs = Transaction.objects.filter(user=user)

    fig = plot_income_expenses_bar_chart(qs)

    # 빈 queryset이어도 Figure 객체는 생성되어야 함
    assert isinstance(fig, go.Figure)
    # None 값들이 들어가야 함 (aggregate에서 None 반환)
    chart_values = fig.data[0].y
    assert chart_values[0] is None
    assert chart_values[1] is None


@pytest.mark.django_db
def test_plot_category_pie_chart_returns_figure(user_transactions):
    """카테고리별 파이 차트가 정상적으로 생성되는지 테스트"""
    user = user_transactions[0].user
    qs = Transaction.objects.filter(user=user, type='income')

    fig = plot_category_pie_chart(qs, '카테고리별 수익합계')

    # plotly Figure 객체가 반환되는지 확인
    assert isinstance(fig, go.Figure)
    # 차트에 데이터가 있는지 확인
    assert len(fig.data) > 0
    # 파이 차트인지 확인
    assert fig.data[0].type == 'pie'

@pytest.mark.django_db
def test_plot_category_pie_chart_aggregates_by_category(user_transactions):
    """파이 차트가 카테고리별로 올바르게 집계하는지 테스트"""
    user = user_transactions[0].user
    qs = Transaction.objects.filter(user=user, type='income')

    # 카테고리별 실제 합계 계산
    from django.db.models import Sum
    expected_data = qs.order_by('category').values_list('category__name').annotate(Sum('amount'))
    expected_categories = [c for c, _ in expected_data]
    expected_amounts = [a for _, a in expected_data]

    fig = plot_category_pie_chart(qs, '테스트')

    # 파이 차트의 labels와 values가 실제 데이터와 일치하는지 확인
    assert list(fig.data[0].labels) == expected_categories
    assert list(fig.data[0].values) == expected_amounts


@pytest.mark.django_db
def test_plot_category_pie_chart_with_empty_queryset(user):
    """빈 queryset으로 파이 차트 생성 시 오류 없이 처리되는지 테스트"""
    qs = Transaction.objects.filter(user=user)

    fig = plot_category_pie_chart(qs, '빈 차트')

    # 빈 queryset이어도 Figure 객체는 생성되어야 함
    assert isinstance(fig, go.Figure)
    # 빈 리스트가 들어가야 함
    assert len(fig.data[0].labels) == 0
    assert len(fig.data[0].values) == 0
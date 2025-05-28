import django_filters
from django import forms
from .models import Transaction, Category

"""
NOTE. filter 사용 시 주의해야 할 점
- filter에 정의한 field name이랑 model의 field name이랑 달라도 된다.
    그치만 view에서 filter 사용할 때 get params은 filter의 filed name으로 적어야 함.
ex) /transactions_list?transaction_type=income (o)
    /transactions_list?type=income (x)
"""

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICE,
        field_name='type',
        lookup_expr='iexact', # sql lookup이랑 대응
        empty_label='전체보기', # 필터 하지 않는 선택항목의 라벨
    )
    start_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte',
        label='시작일',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte',
        label='종료일',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type', 'start_date', 'end_date')
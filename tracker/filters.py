import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    transaction_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICE,
        field_name='type',
        lookup_expr='iexact', # sql loolup이랑 대응
        empty_label='전체보기', # 필터 하지 않는 선택항목의 라벨
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type', )
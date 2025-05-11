import pytest
from models import Transaction

'''
기본적으로 pytest는 django db에 접근을 못함
그래서 pytest-django 패키지를 통해 pytest 메서드가 django test db에 접근할 수 있게 한다
이 경우 conftest에서 만든 transaction 더미 데이터에 접근하기 위해 데코레이터를 사용함
'''
@pytest.mark.django_db
def test_queryset_get_income_method(tranctios):
    pass
import pytest
from tracker.factories import TransactionFactory
"""
- 이렇게 고정(fixture)한 메서드는 다른 테스트에서도 기본적으로 사용할 수 있다
- 테스트에서 사용하는 법: 그냥 함수명을 테스트 함수의 매개변수로 넣으면 됨
"""
@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)
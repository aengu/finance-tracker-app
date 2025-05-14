import pytest
from tracker.factories import TransactionFactory, UserFactory
from tracker.models import User
"""
- 이렇게 고정(fixture)한 메서드는 다른 테스트에서도 기본적으로 사용할 수 있다
- 테스트에서 사용하는 법: 그냥 함수명을 테스트 함수의 매개변수로 넣으면 됨
"""
@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)


@pytest.fixture
def user_transactions():
    test_user = UserFactory()
    return TransactionFactory.create_batch(20, user=test_user) # 생성된 트렉젝션의 모든 user가 test_user로 연결됨
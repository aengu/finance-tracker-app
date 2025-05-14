### factory boy 패키지
- https://factoryboy.readthedocs.io/en/stable/
- 테스트용 더미 데이터를 자동으로 만들어 주는 python 패키지
- django 모델 인스턴스나 다른 객체들을 간단한 코드로 만들 수 있다
- 보통 Pytest와 같이 사용하기 때문에 자동으로 db롤백 되어 테스트 동안 생성한 더미데이터를 수동으로 삭제할 필요는 없다
- 사용방법
    1. 보통 factories.py에 더미 데이터 생성할 모델의 Facory 클래스를 만들고
    2. factory 인스턴스의 batch로 데이터 생성
        ```python
        transaction_factory = TransactionFactory(amount=11.55) # 인수로 재정의 가능
        transaction_factory.create_batch(10)  # 10개 생성
        ```
- 본 프로젝트에선
    0. managers.py: 테스트 할 transaction모델의 income, expense 속성 집계 쿼리셋을 커스텀 
    1. factories.py: 더미데이터 생성 할 팩토리 클래스 정의
    2. conftest.py: 1에서 정의한 팩토리 클래스로 transaction 20개 생성
    3. test_models.py: pytest 테스트 코드


### pytest, django-pytest
- https://docs.pytest.org/en/8.2.x/reference/reference.html
- https://pytest-django.readthedocs.io/en/latest/


- Pytest
    - Python에서 가장 널리 사용되는 테스트 프레임워크
    - 간결한 문법과 강력한 fixture 기능 제공
    - assert 구문 그대로 사용 가능
    - pytest-mock 같은 플러그인과 쉽게 통합됨

- Pytest-Django
    - Django 프로젝트에서 pytest를 쓸 수 있게 도와주는 플러그인
    - Django의 DB, client, 설정 등을 pytest에 통합해줌

- Pytest vs Django TestCase

| 항목      | Pytest                      | Django TestCase        |
| ------- | --------------------------- | ---------------------- |
| 구조      | 함수 기반                       | 클래스 기반                 |
| DB 접근   | `@pytest.mark.django_db` 필요 | 자동 가능                  |
| fixture | 매우 유연하고 재사용 쉬움              | `setUp()` 메서드 제한적      |
| assert  | Python 기본 assert 사용         | `self.assertEqual()` 등 |

---

